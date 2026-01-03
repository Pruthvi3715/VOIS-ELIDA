"""
Authentication endpoints for user registration and login.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from datetime import timedelta

from app.database import get_db
from app.models.db_models import User, InvestorProfile
from app.auth.auth import hash_password, verify_password, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/api/auth", tags=["authentication"])

# Request/Response models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.
    Creates user account and default investor profile.
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default investor profile
    default_profile = InvestorProfile(
        user_id=new_user.id,
        risk_tolerance="moderate",
        time_horizon=5,
        investment_goals=["growth"],
        sectors=[],
        custom_rules=[]
    )
    db.add(default_profile)
    db.commit()
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "username": new_user.username}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=new_user.id,
        username=new_user.username
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with username and password.
    Returns JWT access token.
    """
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Generate JWT token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.id,
        username=user.username
    )
