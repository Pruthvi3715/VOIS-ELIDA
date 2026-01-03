"""
Profile management router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.database import get_db
from app.auth.auth import get_current_user_id
from app.services.profile_service import profile_service

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])


class ProfileUpdate(BaseModel):
    risk_tolerance: Optional[str] = None
    time_horizon: Optional[int] = None
    investment_goals: Optional[List[str]] = None
    sectors: Optional[List[str]] = None
    custom_rules: Optional[List[str]] = None


@router.get("/me")
def get_my_profile(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Get current user's investor profile."""
    profile = profile_service.get_profile_by_user_id(db, user_id)
    return profile


@router.post("")
def update_profile(
    profile_data: ProfileUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Update current user's investor profile."""
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    updated = profile_service.update_profile(db, user_id_int, profile_data.model_dump(exclude_none=True))
    return updated
