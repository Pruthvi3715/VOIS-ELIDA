"""
Portfolio Service - Manages portfolio analysis requests.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from sqlalchemy.orm import Session
from app.models.db_models import PortfolioRequest
from app.models.investor_dna import InvestorDNA


class PortfolioService:
    """Service for managing portfolio analysis."""
    
    def create_request(self, db: Session, user_id: int, tickers: List[str]) -> str:
        """Create a new portfolio analysis request."""
        request_id = str(uuid.uuid4())[:8]
        
        request = PortfolioRequest(
            request_id=request_id,
            user_id=user_id,
            tickers=tickers,
            status="pending"
        )
        db.add(request)
        db.commit()
        
        return request_id
    
    def get_status(self, db: Session, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a portfolio request."""
        request = db.query(PortfolioRequest).filter(
            PortfolioRequest.request_id == request_id
        ).first()
        
        if not request:
            return None
        
        return {
            "request_id": request.request_id,
            "status": request.status,
            "tickers": request.tickers,
            "results": request.results or {},
            "created_at": request.created_at.isoformat() if request.created_at else None,
            "completed_at": request.completed_at.isoformat() if request.completed_at else None
        }
    
    def update_status(self, db: Session, request_id: str, status: str, results: Dict = None):
        """Update request status."""
        request = db.query(PortfolioRequest).filter(
            PortfolioRequest.request_id == request_id
        ).first()
        
        if request:
            request.status = status
            if results:
                request.results = results
            if status == "completed":
                request.completed_at = datetime.utcnow()
            db.commit()
    
    async def process_portfolio_async(
        self,
        session_factory: Callable,
        request_id: str,
        user_id: int,
        tickers: List[str],
        profile: InvestorDNA
    ):
        """Process portfolio analysis in background."""
        db = session_factory()
        try:
            self.update_status(db, request_id, "processing")
            
            results = {}
            from app.orchestrator import orchestrator
            
            for ticker in tickers:
                try:
                    # Ingest and analyze
                    orchestrator.ingest_asset(ticker)
                    analysis = orchestrator.retrieve_context(
                        query="comprehensive analysis",
                        asset_id=ticker,
                        investor_dna=profile
                    )
                    results[ticker] = {
                        "status": "success",
                        "analysis": analysis
                    }
                except Exception as e:
                    results[ticker] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            self.update_status(db, request_id, "completed", results)
        except Exception as e:
            self.update_status(db, request_id, "failed", {"error": str(e)})
        finally:
            db.close()


portfolio_service = PortfolioService()
