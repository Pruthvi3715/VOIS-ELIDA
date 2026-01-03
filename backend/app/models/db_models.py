"""
Database models for ELIDA - Users, Profiles, and History.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    profile = relationship("InvestorProfile", back_populates="user", uselist=False)
    history = relationship("AnalysisHistory", back_populates="user")


class InvestorProfile(Base):
    """Investor DNA/Profile model."""
    __tablename__ = "investor_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    risk_tolerance = Column(String(20), default="moderate")  # conservative, moderate, aggressive
    time_horizon = Column(Integer, default=5)  # years
    investment_goals = Column(JSON, default=list)  # ["growth", "income", "preservation"]
    sectors = Column(JSON, default=list)  # ["technology", "healthcare", etc.]
    custom_rules = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")


class AnalysisHistory(Base):
    """Analysis history model."""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query_type = Column(String(50))  # "analysis", "search", "chat"
    query = Column(Text)  # asset_id or search query
    result = Column(JSON)  # Full analysis result
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="history")


class PortfolioRequest(Base):
    """Portfolio scan request tracking."""
    __tablename__ = "portfolio_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(50), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tickers = Column(JSON)  # List of tickers
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    results = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
