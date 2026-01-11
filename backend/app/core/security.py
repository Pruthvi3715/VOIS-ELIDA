"""
Security utilities for ELIDA API.
Includes rate limiting and input validation.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re
import html

# ============== RATE LIMITING ==============

def get_user_or_ip(request: Request) -> str:
    """
    Get rate limit key from authenticated user or IP address.
    Prioritizes user_id if available, falls back to IP.
    """
    # Try to get user from auth header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        # Extract user from token (simplified - in production decode JWT)
        # For now, use the token hash as identifier
        token = auth_header[7:]
        if len(token) > 10:
            return f"user:{token[:20]}"
    
    # Fallback to IP address
    return get_remote_address(request)

# Create limiter with combined user/IP key
limiter = Limiter(key_func=get_user_or_ip)

# Rate limit configurations
RATE_LIMITS = {
    "default": "100/minute",
    "analysis": "10/minute",      # Heavy LLM operations
    "chat": "30/minute",          # Moderate LLM operations
    "auth": "5/minute",           # Prevent brute force
    "market_data": "60/minute",   # Lightweight data fetch
}


# ============== INPUT VALIDATION ==============

# Allowed characters for stock tickers
TICKER_PATTERN = re.compile(r'^[A-Z0-9\.\-]{1,20}$', re.IGNORECASE)

# Max lengths for various inputs
MAX_TICKER_LENGTH = 20
MAX_QUERY_LENGTH = 500
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 128


def sanitize_string(value: str, max_length: int = 500) -> str:
    """
    Sanitize string input:
    - Strip whitespace
    - Escape HTML entities
    - Truncate to max length
    """
    if not value:
        return ""
    
    # Strip and truncate
    value = value.strip()[:max_length]
    
    # Escape HTML to prevent XSS
    value = html.escape(value)
    
    return value


def validate_ticker(ticker: str) -> str:
    """
    Validate stock ticker format.
    Raises HTTPException for invalid tickers.
    """
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker symbol is required")
    
    ticker = ticker.strip().upper()
    
    if len(ticker) > MAX_TICKER_LENGTH:
        raise HTTPException(status_code=400, detail=f"Ticker too long (max {MAX_TICKER_LENGTH} chars)")
    
    if not TICKER_PATTERN.match(ticker):
        raise HTTPException(
            status_code=400, 
            detail="Invalid ticker format. Use letters, numbers, dots, and hyphens only."
        )
    
    return ticker


def validate_query(query: str) -> str:
    """
    Validate and sanitize user query input.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    query = sanitize_string(query, MAX_QUERY_LENGTH)
    
    if len(query) < 2:
        raise HTTPException(status_code=400, detail="Query too short (min 2 chars)")
    
    return query


# ============== PYDANTIC MODELS WITH VALIDATION ==============

class SecureAnalysisRequest(BaseModel):
    """Validated analysis request model."""
    ticker: str = Field(..., min_length=1, max_length=20)
    demo: bool = False
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker_format(cls, v):
        v = v.strip().upper()
        if not TICKER_PATTERN.match(v):
            raise ValueError("Invalid ticker format")
        return v


class SecureChatRequest(BaseModel):
    """Validated chat request model."""
    query: str = Field(..., min_length=2, max_length=500)
    user_id: Optional[str] = Field(default="default", max_length=50)
    
    @field_validator('query')
    @classmethod
    def sanitize_query(cls, v):
        return html.escape(v.strip())


class SecureLoginRequest(BaseModel):
    """Validated login request model."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        v = v.strip()
        # Only allow alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v


class SecureRegisterRequest(BaseModel):
    """Validated registration request model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        v = v.strip()
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError("Username can only contain letters, numbers, and underscores")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        v = v.strip().lower()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError("Invalid email format")
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        # Check for at least one number and one letter
        if not re.search(r'[A-Za-z]', v) or not re.search(r'[0-9]', v):
            raise ValueError("Password must contain both letters and numbers")
        return v


# ============== SECURITY HEADERS MIDDLEWARE ==============

async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Prevent XSS
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Content Security Policy (adjust as needed)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response
