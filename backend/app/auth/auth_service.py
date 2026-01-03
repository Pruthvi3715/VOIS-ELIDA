"""
Authentication Service for VOIS Financial System
Handles JWT token generation, validation, and user management
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    user_id: str
    email: Optional[str] = None


class UserCreate(BaseModel):
    user_id: str
    email: str
    password: str


class UserLogin(BaseModel):
    user_id: str
    password: str


class AuthService:
    """Handles authentication operations"""
    
    def __init__(self):
        # In-memory user storage for MVP (migrate to database later)
        self.users = {
            "default": {
                "user_id": "default",
                "email": "demo@vois.ai",
                "hashed_password": self.hash_password("demo123")
            }
        }
    
    def hash_password(self, password: str) -> str:
        """Hash a password for storage"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, user_data: UserCreate) -> dict:
        """Create a new user"""
        if user_data.user_id in self.users:
            raise ValueError(f"User {user_data.user_id} already exists")
        
        self.users[user_data.user_id] = {
            "user_id": user_data.user_id,
            "email": user_data.email,
            "hashed_password": self.hash_password(user_data.password)
        }
        
        return {
            "user_id": user_data.user_id,
            "email": user_data.email
        }
    
    def authenticate_user(self, user_id: str, password: str) -> Optional[dict]:
        """Authenticate user with password"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        if not self.verify_password(password, user["hashed_password"]):
            return None
        
        return {
            "user_id": user["user_id"],
            "email": user["email"]
        }
    
    def create_access_token(self, user_id: str, email: str = None) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user_id,
            "email": email,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[TokenData]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            
            if user_id is None:
                return None
            
            return TokenData(user_id=user_id, email=email)
        except jwt.PyJWTError:
            return None
    
    def get_current_user(self, token: str) -> Optional[dict]:
        """Get current user from token"""
        token_data = self.decode_token(token)
        if not token_data:
            return None
        
        user = self.users.get(token_data.user_id)
        if not user:
            return None
        
        return {
            "user_id": user["user_id"],
            "email": user["email"]
        }


auth_service = AuthService()
