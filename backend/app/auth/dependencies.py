"""
Authentication middleware and dependencies for FastAPI
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_service import auth_service
from typing import Optional

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to extract and validate user from JWT token.
    Use this in endpoints that require authentication.
    
    Example:
        @app.get("/protected")
        def protected_route(user_id: str = Depends(get_current_user_id)):
            return {"message": f"Hello {user_id}"}
    """
    token = credentials.credentials
    user = auth_service.get_current_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user["user_id"]


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[str]:
    """
    Optional authentication dependency.
    Returns user_id if authenticated, "default" otherwise.
    
    Use for endpoints that work with user_id="default" for unauthenticated users.
    """
    if not credentials:
        return "default"
    
    token = credentials.credentials
    user = auth_service.get_current_user(token)
    
    return user["user_id"] if user else "default"
