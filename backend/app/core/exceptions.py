"""
Custom exceptions for ELIDA.
Provides specific exception types for better error handling and debugging.
"""
from typing import Optional, Dict, Any


class ElidaException(Exception):
    """Base exception for all ELIDA errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": self.message,
            "type": self.__class__.__name__,
            "details": self.details
        }


class DataFetchException(ElidaException):
    """Failed to fetch market data from external APIs."""
    
    def __init__(self, asset_id: str, source: str, reason: str):
        super().__init__(
            f"Failed to fetch data for {asset_id} from {source}: {reason}",
            {"asset_id": asset_id, "source": source, "reason": reason}
        )


class AgentException(ElidaException):
    """An analysis agent failed to process."""
    
    def __init__(self, agent_name: str, reason: str, context: Optional[str] = None):
        super().__init__(
            f"Agent '{agent_name}' failed: {reason}",
            {"agent": agent_name, "reason": reason, "context": context}
        )


class LLMException(ElidaException):
    """LLM call failed (Ollama, Groq, Gemini, etc.)."""
    
    def __init__(self, provider: str, reason: str, model: Optional[str] = None):
        super().__init__(
            f"LLM call to {provider} failed: {reason}",
            {"provider": provider, "model": model, "reason": reason}
        )


class RAGException(ElidaException):
    """RAG service operation failed."""
    
    def __init__(self, operation: str, reason: str):
        super().__init__(
            f"RAG {operation} failed: {reason}",
            {"operation": operation, "reason": reason}
        )


class AuthException(ElidaException):
    """Authentication or authorization failed."""
    
    def __init__(self, reason: str, user_id: Optional[str] = None):
        super().__init__(
            f"Authentication failed: {reason}",
            {"reason": reason, "user_id": user_id}
        )


class ValidationException(ElidaException):
    """Input validation failed."""
    
    def __init__(self, field: str, reason: str, value: Optional[Any] = None):
        super().__init__(
            f"Validation failed for '{field}': {reason}",
            {"field": field, "reason": reason, "value": str(value) if value else None}
        )


class OrchestrationException(ElidaException):
    """Analysis orchestration failed."""
    
    def __init__(self, asset_id: str, phase: str, reason: str):
        super().__init__(
            f"Orchestration failed for {asset_id} during {phase}: {reason}",
            {"asset_id": asset_id, "phase": phase, "reason": reason}
        )
