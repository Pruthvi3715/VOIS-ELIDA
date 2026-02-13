"""
Test fixtures and configuration for ELIDA backend tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.db_models import User, InvestorProfile, AnalysisHistory
from app.models.investor_dna import InvestorDNA, DEFAULT_INVESTOR_DNA


# Test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user(test_db):
    """Create a sample user for testing."""
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$test_hash",
        username="testuser"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_investor_dna():
    """Sample InvestorDNA for testing."""
    return InvestorDNA(
        risk_tolerance="Moderate",
        investment_horizon="Medium Term (3-7 years)",
        investment_goals=["Retirement", "Wealth Growth"],
        preferred_sectors=["Technology", "Finance"],
        ethical_filters={"prevent_tobacco": True, "prevent_weapons": False},
        custom_rules=["No penny stocks"]
    )


@pytest.fixture
def sample_context():
    """Sample RAG context for agent testing."""
    return [
        {
            "content": """{'company_name': 'Test Corp', 'current_price': 100.0, 
            'pe_ratio': 25.0, 'roe': 15.0, 'debt_to_equity': 0.5, 
            'revenue_growth': 10.0, 'profit_margin': 12.0}""",
            "metadata": {"type": "financials", "asset_id": "TEST"}
        },
        {
            "content": """{'rbi_rate': 6.5, 'inflation': 5.0, 'usd_inr': 83.0,
            'vix': 15.0, 'sector': 'Technology'}""",
            "metadata": {"type": "macro", "asset_id": "GLOBAL"}
        }
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing without actual API calls."""
    return {
        "score": 75,
        "confidence": 80,
        "analysis": "Test analysis result from mock LLM.",
        "reasoning": "Mock reasoning for testing purposes."
    }
