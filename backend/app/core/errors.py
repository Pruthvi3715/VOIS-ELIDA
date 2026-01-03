"""
Custom exception classes for ELIDA application.
"""
from fastapi import HTTPException


class AppException(Exception):
    """Base application exception with status code and error code."""
    def __init__(self, message: str, status_code: int = 500, code: str = "APP_ERROR"):
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(self.message)


class ResourceNotFound(AppException):
    """Resource not found exception (404)."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404, code="NOT_FOUND")


class InvalidRequest(AppException):
    """Invalid request exception (400)."""
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message=message, status_code=400, code="INVALID_REQUEST")


class LLMGenerationError(AppException):
    """LLM generation failed exception (500)."""
    def __init__(self, message: str = "LLM generation failed"):
        super().__init__(message=message, status_code=500, code="LLM_ERROR")


class AuthenticationError(AppException):
    """Authentication failed exception (401)."""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message=message, status_code=401, code="AUTH_ERROR")
