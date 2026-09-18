from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db_session_dep
from app.db.repositories import ContactRepository

router = APIRouter()

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/contact", response_model=dict)
async def submit_contact(
    request: ContactRequest,
    db: AsyncSession = Depends(get_db_session_dep),
):
    try:
        contact_repo = ContactRepository(db)
        contact_id = await contact_repo.add_contact(
            request.name, request.email, request.message
        )
        await db.commit()

        return {
            "success": True,
            "message": "Contact message submitted successfully",
            "contact_id": str(contact_id)
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
