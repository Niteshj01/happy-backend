from passlib.context import CryptContext
import os
from typing import Optional
import logging
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection for admin credentials
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

async def get_admin_from_db(username: str) -> Optional[dict]:
    """Get admin user from database"""
    return await db.admin_users.find_one({"username": username})

async def verify_admin_credentials(username: str, password: str) -> bool:
    """
    Verify admin credentials against database
    Returns True if credentials are valid
    """
    # Get admin from database
    admin = await get_admin_from_db(username)
    
    # If no admin exists, create default admin with password 'admin123'
    if not admin:
        logger.warning("No admin user found in database. Creating default admin.")
        default_hash = get_password_hash('admin123')
        await db.admin_users.insert_one({
            "username": "admin",
            "password_hash": default_hash,
            "created_at": "2024-01-01T00:00:00Z"
        })
        admin = await get_admin_from_db("admin")
    
    if not admin:
        return False
    
    # Verify password
    return verify_password(password, admin['password_hash'])

async def change_admin_password(old_password: str, new_password: str, username: str) -> tuple[bool, str]:
    """
    Change admin password in database
    Returns (success: bool, message: str)
    """
    # Verify old password first
    is_valid = await verify_admin_credentials(username, old_password)
    if not is_valid:
        return False, "Current password is incorrect"
    
    # Hash new password
    new_hash = get_password_hash(new_password)
    
    # Update password in database
    result = await db.admin_users.update_one(
        {"username": username},
        {"$set": {"password_hash": new_hash}}
    )
    
    if result.modified_count > 0:
        return True, "Password changed successfully"
    else:
        return False, "Failed to update password"

def get_default_password_hash() -> str:
    """Get hash for default password (admin123)"""
    return get_password_hash('admin123')
