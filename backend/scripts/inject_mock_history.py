import sys
import os
import json
from datetime import datetime

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.db_models import User, AnalysisHistory

def inject_mock_data():
    db = SessionLocal()
    try:
        # Get first user (usually 'testuser')
        user = db.query(User).first()
        if not user:
            print("❌ No user found! Please register/login first.")
            return

        print(f"✅ Found user: {user.username} (ID: {user.id})")

        # Mock Analysis Result
        mock_result = {
            "asset_id": "AAPL",
            "company_name": "Apple Inc.",
            "current_price": 185.92,
            "currency": "USD",
            "overall_score": 88,
            "recommendation": "Strong Buy",
            "summary": "Apple continues to demonstrate robust fundamentals with a fortress balance sheet.",
            "analysis_date": datetime.utcnow().isoformat(),
            "agent_details": [
                {"name": "Quant Agent", "score": 92, "signal": "bullish", "details": "Strong ROE of 160% and massive cash reserves."},
                {"name": "Macro Agent", "score": 85, "signal": "bullish", "details": "Tech sector showing resilience despite rate headwinds."},
                {"name": "Philosopher Agent", "score": 80, "signal": "neutral", "details": "Good governance but supply chain concerns persist."},
                {"name": "Regret Agent", "score": 95, "signal": "bullish", "details": "Low probability of catastrophic failure."},
            ],
            "coach_verdict": "A cornerstone holding for any portfolio. The valuation is premium but justified by quality."
        }

        # Create History Entry
        entry = AnalysisHistory(
            user_id=user.id,
            query_type="analysis",
            query="AAPL",
            result=mock_result,
            created_at=datetime.utcnow()
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)

        print(f"✅ Successfully injected mock history for AAPL!")
        print(f"   Entry ID: {entry.id}")
        print(f"   Timestamp: {entry.created_at}")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    inject_mock_data()
