"""
History management router.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

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
    
    # FIX: Correct method name and arguments
    entries = history_service.get_user_history(user_id=user_id_int, db=db, limit=limit)
    return {"entries": entries}


@router.get("/{entry_id}")
def get_history_entry(
    entry_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get full details of a specific history entry."""
    entry = history_service.get_entry(entry_id, db)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.delete("/{entry_id}")
def delete_history_entry(
    entry_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Delete a history entry."""
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")
        
    # Note: Service currently doesn't check user_id for delete, but we should ideally
    success = history_service.delete_entry(entry_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"status": "deleted"}


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
    
    # FIX: save_entry returns the ID directly (int)
    entry_id = history_service.save_entry(
        db=db,
        user_id=user_id_int,
        query_type=entry.query_type,
        query=entry.query,
        result=entry.result
    )
    return {"status": "saved", "entry_id": entry_id}
