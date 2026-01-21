from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
from enum import Enum
from email_service import send_appointment_confirmation_email
from auth_service import verify_admin_credentials, change_admin_password, get_password_hash


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Enums
class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class ImageCategory(str, Enum):
    clinic = "clinic"
    equipment = "equipment"
    team = "team"
    patients = "patients"


# Define Models
class AppointmentCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = None
    date: str
    time: Optional[str] = None
    service: str
    message: Optional[str] = None

class Appointment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    phone: str
    email: Optional[str] = None
    date: str
    time: Optional[str] = None
    service: str
    message: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.pending
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus

class GalleryImageCreate(BaseModel):
    url: str
    title: str
    category: ImageCategory

class GalleryImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    url: str
    title: str
    category: ImageCategory
    createdAt: datetime = Field(default_factory=datetime.utcnow)

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminPasswordChange(BaseModel):
    username: str
    old_password: str
    new_password: str

class AdminPasswordChangeResponse(BaseModel):
    success: bool
    message: str
    new_password_hash: Optional[str] = None


# Appointment Routes
@api_router.post("/appointments", response_model=Appointment)
async def create_appointment(appointment_data: AppointmentCreate):
    appointment = Appointment(**appointment_data.dict())
    await db.appointments.insert_one(appointment.dict())
    return appointment

@api_router.get("/appointments", response_model=List[Appointment])
async def get_appointments():
    appointments = await db.appointments.find().sort("createdAt", -1).to_list(1000)
    return [Appointment(**appointment) for appointment in appointments]

@api_router.patch("/appointments/{appointment_id}/status", response_model=Appointment)
async def update_appointment_status(appointment_id: str, status_update: AppointmentStatusUpdate):
    appointment = await db.appointments.find_one({"id": appointment_id})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    await db.appointments.update_one(
        {"id": appointment_id},
        {"$set": {"status": status_update.status.value}}
    )
    
    updated_appointment = await db.appointments.find_one({"id": appointment_id})
    
    # Send confirmation email if status is confirmed and email exists
    if status_update.status.value == "confirmed" and updated_appointment.get("email"):
        try:
            email_sent = send_appointment_confirmation_email(
                appointment_data=updated_appointment,
                recipient_email=updated_appointment["email"]
            )
            if email_sent:
                logger.info(f"Confirmation email sent for appointment {appointment_id}")
            else:
                logger.warning(f"Email not sent for appointment {appointment_id} - SMTP not configured")
        except Exception as e:
            # Don't fail the request if email fails
            logger.error(f"Error sending email for appointment {appointment_id}: {str(e)}")
    
    return Appointment(**updated_appointment)

@api_router.delete("/appointments/{appointment_id}")
async def delete_appointment(appointment_id: str):
    result = await db.appointments.delete_one({"id": appointment_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}


# Gallery Routes
@api_router.get("/gallery", response_model=List[GalleryImage])
async def get_gallery_images():
    images = await db.gallery_images.find().sort("createdAt", -1).to_list(1000)
    return [GalleryImage(**image) for image in images]

@api_router.post("/gallery", response_model=GalleryImage)
async def create_gallery_image(image_data: GalleryImageCreate):
    image = GalleryImage(**image_data.dict())
    await db.gallery_images.insert_one(image.dict())
    return image

@api_router.delete("/gallery/{image_id}")
async def delete_gallery_image(image_id: str):
    result = await db.gallery_images.delete_one({"id": image_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"message": "Image deleted successfully"}


# Health check route
@api_router.get("/")
async def root():
    return {"message": "Happy Teeth Dental Clinic API", "status": "active"}

# Admin Authentication Routes
@api_router.post("/admin/login")
async def admin_login(credentials: AdminLogin):
    """Verify admin credentials"""
    is_valid = await verify_admin_credentials(credentials.username, credentials.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "message": "Login successful"}

@api_router.post("/admin/change-password", response_model=AdminPasswordChangeResponse)
async def admin_change_password(password_change: AdminPasswordChange):
    """
    Change admin password - now updates database directly
    """
    success, message = await change_admin_password(
        password_change.old_password,
        password_change.new_password,
        password_change.username
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return AdminPasswordChangeResponse(
        success=True,
        message="Password changed successfully! You can now login with your new password.",
        new_password_hash=None  # No longer needed as it's stored in DB
    )

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()