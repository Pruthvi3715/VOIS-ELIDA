from sqlalchemy.orm import Session
from app.models.db_models import AnalysisHistory
from datetime import datetime
from typing import List, Dict, Optional

class HistoryService:
    def save_entry(self, db: Session, user_id: int, query_type: str, query: str, result: Dict) -> int:
        """
        Save a new history entry.
        query_type: 'analysis' | 'search'
        """
        entry = AnalysisHistory(
            user_id=user_id,
            query_type=query_type,
            query=query,
            result=result,
            created_at=datetime.utcnow()
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry.id

    def get_user_history(self, user_id: int, db: Session, limit: int = 20) -> List[Dict]:
        """Get summary history for a user."""
        history = db.query(AnalysisHistory)\
            .filter(AnalysisHistory.user_id == user_id)\
            .order_by(AnalysisHistory.created_at.desc())\
            .limit(limit)\
            .all()
            
        return [
            {
                "id": str(h.id),
                "type": h.query_type,
                "query": h.query,
                "timestamp": h.created_at.isoformat()
            }
            for h in history
        ]

    def get_entry(self, entry_id: int, db: Session) -> Optional[Dict]:
        """Get full details of a specific entry."""
        item = db.query(AnalysisHistory).filter(AnalysisHistory.id == entry_id).first()
        if item:
            return {
                "id": str(item.id),
                "user_id": str(item.user_id),
                "type": item.query_type,
                "query": item.query,
                "timestamp": item.created_at.isoformat(),
                "result": item.result
            }
        return None

    def delete_entry(self, entry_id: int, db: Session) -> bool:
        """Delete a history entry."""
        item = db.query(AnalysisHistory).filter(AnalysisHistory.id == entry_id).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False

# Singleton instance
history_service = HistoryService()
