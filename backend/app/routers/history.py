"""
History management router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.auth.auth import get_current_user_id
from app.services.history_service import history_service

router = APIRouter(prefix="/api/v1/history", tags=["history"])


@router.get("")
def get_history(
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get user's analysis history."""
    try:
        user_id_int = int(user_id)
    except ValueError:
        return {"entries": [], "message": "Invalid user ID"}
    
    entries = history_service.get_history(db, user_id_int, limit)
    return {"entries": entries}


    success = history_service.delete_entry(db, entry_id, user_id_int)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"status": "deleted"}

from pydantic import BaseModel
from typing import Dict, Any

class CreateHistoryEntry(BaseModel):
    query_type: str
    query: str
    result: Dict[str, Any]

@router.post("")
def save_history_entry(
    entry: CreateHistoryEntry,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Manually save a history entry."""
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    saved_entry = history_service.save_entry(
        db=db,
        user_id=user_id_int,
        query_type=entry.query_type,
        query=entry.query,
        result=entry.result
    )
    return {"status": "saved", "entry_id": saved_entry.id}
