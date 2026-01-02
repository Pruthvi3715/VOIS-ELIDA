
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class HistoryService:
    def __init__(self, data_file: str = "data/history.json"):
        self.data_file = Path(data_file)
        self._ensure_file()

    def _ensure_file(self):
        """Ensure data file and directory exist."""
        if not self.data_file.parent.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, "w") as f:
                json.dump([], f)

    def _read_data(self) -> List[Dict]:
        """Read all history data."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_data(self, data: List[Dict]):
        """Write data to history file."""
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2)

    def save_entry(self, user_id: str, query_type: str, query: str, result: Dict) -> str:
        """
        Save a new history entry.
        query_type: 'analysis' | 'search'
        """
        entry_id = str(uuid.uuid4())
        entry = {
            "id": entry_id,
            "user_id": user_id,
            "type": query_type,
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "result": result
        }
        
        history = self._read_data()
        history.insert(0, entry) # Prepend to keep latest first
        
        # Limit history size per user/file (optional, keep simple for now)
        if len(history) > 1000:
            history = history[:1000]
            
        self._write_data(history)
        return entry_id

    def get_user_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get summary history for a user."""
        history = self._read_data()
        user_history = [
            {
                "id": item["id"],
                "type": item["type"],
                "query": item["query"],
                "timestamp": item["timestamp"]
            }
            for item in history if item["user_id"] == user_id
        ]
        return user_history[:limit]

    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Get full details of a specific entry."""
        history = self._read_data()
        for item in history:
            if item["id"] == entry_id:
                return item
        return None

# Singleton instance
history_service = HistoryService()
