from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/contact", response_model=dict)
async def submit_contact(request: ContactRequest):
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        from datetime import datetime
        
        client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_DB_NAME]
        contact_collection = db["contacts"]
        
        contact = {
            "name": request.name,
            "email": request.email,
            "message": request.message,
            "created_at": datetime.utcnow()
        }
        
        result = await contact_collection.insert_one(contact)
        await client.close()
        
        return {
            "success": True,
            "message": "Contact message submitted successfully",
            "contact_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
