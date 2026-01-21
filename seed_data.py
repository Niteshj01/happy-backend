import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initial gallery images
initial_images = [
    {
        'id': '1',
        'url': 'https://images.unsplash.com/photo-1629909613654-28e377c37b09?w=800&q=80',
        'title': 'Modern Dental Clinic',
        'category': 'clinic',
        'createdAt': '2024-01-01T00:00:00Z'
    },
    {
        'id': '2',
        'url': 'https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?w=800&q=80',
        'title': 'State-of-the-Art Equipment',
        'category': 'equipment',
        'createdAt': '2024-01-02T00:00:00Z'
    },
    {
        'id': '3',
        'url': 'https://images.unsplash.com/photo-1606811971618-4486d14f3f99?w=800&q=80',
        'title': 'Comfortable Treatment Room',
        'category': 'clinic',
        'createdAt': '2024-01-03T00:00:00Z'
    },
    {
        'id': '4',
        'url': 'https://images.unsplash.com/photo-1598256989800-fe5f95da9787?w=800&q=80',
        'title': 'Professional Dental Team',
        'category': 'team',
        'createdAt': '2024-01-04T00:00:00Z'
    },
    {
        'id': '5',
        'url': 'https://images.unsplash.com/photo-1609840112855-9ab5ad8f66e4?w=800&q=80',
        'title': 'Advanced Dental Technology',
        'category': 'equipment',
        'createdAt': '2024-01-05T00:00:00Z'
    },
    {
        'id': '6',
        'url': 'https://images.unsplash.com/photo-1588776814546-daab30f310ce?w=800&q=80',
        'title': 'Happy Patient Care',
        'category': 'patients',
        'createdAt': '2024-01-06T00:00:00Z'
    }
]

async def seed_gallery():
    # Check if gallery already has images
    count = await db.gallery_images.count_documents({})
    if count > 0:
        print(f"Gallery already has {count} images. Skipping seed.")
        return
    
    # Insert initial images
    await db.gallery_images.insert_many(initial_images)
    print(f"Successfully seeded {len(initial_images)} gallery images!")

async def main():
    try:
        await seed_gallery()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
