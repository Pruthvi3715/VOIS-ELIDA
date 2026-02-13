from typing import Optional, Literal
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "ELIDA - Financial Decision Support System"
    API_V1_STR: str = "/api/v1"
    
    # Production Readiness
    ALLOW_DEMO_DATA: bool = True  # Enable for demo/presentation - uses cached data when APIs fail
    
    # API Keys (Optional if using local LLM)
    GEMINI_API_KEY: Optional[str] = None
    FRED_API_KEY: Optional[str] = None
    
    # LLM Configuration
    # Use Ollama for local LLM (no API key needed)
    LLM_PROVIDER: Literal["auto", "ollama", "gemini", "groq", "claude", "openrouter"] = "ollama"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openrouter/pony-alpha"
    
    GROQ_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    # Groq Llama 8B Instant - fast inference
    GROQ_MODEL: str = Field(default="llama-3.1-8b-instant", validation_alias="OVERRIDE_GROQ_MODEL")
    
    # Database
    DATABASE_URL: str = "sqlite:///./elida.db"
    
    # JWT Authentication
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    model_config = {"env_file": ".env", "extra": "ignore", "case_sensitive": True}

settings = Settings()
