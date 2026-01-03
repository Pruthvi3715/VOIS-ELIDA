from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
import time
from unittest.mock import MagicMock, patch

# Env setup before imports
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "testsubset"

# Mock Orchestrator to avoid real LLM calls
with patch("app.orchestrator.orchestrator") as mock_orch:
    # Setup mock returns
    mock_orch.ingest_asset.return_value = {"status": "ingested"}
    mock_orch.retrieve_context.return_value = {
        "match_result": {
            "score": 85,
            "recommendation": "Buy", 
            "risk_assessment": {"risk_level": "Low"}
        }
    }
    
    from app.main import app
    from app.database import Base, get_db

    # Setup Test DB
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Override Dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Ensure models are loaded
    from app.models.db_models import User, InvestorProfile, AnalysisRequest

    # Create tables
    Base.metadata.create_all(bind=engine)

    client = TestClient(app)

    def test_global_error_handling():
        # Test 404 for non-existent endpoint
        response = client.get("/api/non_existent")
        assert response.status_code == 404
        # Standard 404 is handled by FastAPI default, 
        # but let's test our custom exception if triggered manually or via logic
        # For now, let's trigger a known endpoint error
        
        # /api/portfolio/status/{request_id} with invalid ID -> 404 custom
        response = client.get("/api/portfolio/status/invalid_uuid")
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["code"] == "RESOURCE_NOT_FOUND"

    def test_async_portfolio_flow():
        # 1. Register/Login user (need simple user setup)
        # We can bypass auth if we mock it or just use an int ID if endpoint allows
        # But endpoints use Depends(get_db) and look up user.
        # Let's create a user directly in DB
        from app.models.db_models import User, InvestorProfile
        db = TestingSessionLocal()
        user = User(username="async_test", email="async@test.com", hashed_password="pw")
        db.add(user)
        db.commit()
        db.refresh(user)
        # Create profile
        profile = InvestorProfile(user_id=user.id)
        db.add(profile)
        db.commit()
        user_id = user.id
        db.close()
        
        # 2. Submit Analysis Request
        scan_payload = {
            "user_id": str(user_id),
            "tickers": ["AAPL", "GOOGL"]
        }
        
        # We need to ensure the background task actually runs. 
        # TestClient handles BackgroundTasks synchronously usually, 
        # but our service creates a NEW session. sqlite memory might not share across threads easily 
        # unless check_same_thread=False is set (which we did).
        
        # We also need to patch SessionLocal in main.py or ensure app uses our TestingSessionLocal factory
        # The background task uses `SessionLocal` imported in main.py. 
        # We should patch `app.services.portfolio_service.SessionLocal` or `app.main.SessionLocal`?
        # Actually `app.main` passes `SessionLocal` to `process_portfolio_async`.
        # We need to patch `app.main.SessionLocal` to be `TestingSessionLocal`.
        
        with patch("app.main.SessionLocal", TestingSessionLocal):
            response = client.post("/api/portfolio/scan", json=scan_payload)
            assert response.status_code == 200
            data = response.json()
            request_id = data["request_id"]
            assert data["status"] == "pending"
            
            # 3. Poll Status
            # Since TestClient runs background tasks synchronously after the response,
            # the task should be complete immediately after the request returns in testing?
            # Actually Starlette TestClient runs background tasks.
            
            response = client.get(f"/api/portfolio/status/{request_id}")
            assert response.status_code == 200
            status_data = response.json()
            
            # It might be "processing" or "completed" depending on execution speed/order
            # But since we mocked orchestrator, it should be fast.
            # Assert valid status
            assert status_data["status"] in ["processing", "completed"]
            
            if status_data["status"] == "completed":
                assert status_data["progress"] == "2/2"
                assert len(status_data["result"]["results"]) == 2
