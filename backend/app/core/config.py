from typing import Optional, Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ELIDA - Financial Decision Support System"
    API_V1_STR: str = "/api/v1"
    
    # API Keys (Required)
    GEMINI_API_KEY: str
    FRED_API_KEY: str
    
    # LLM Configuration
    LLM_PROVIDER: Literal["auto", "ollama", "gemini", "groq"] = "auto"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OLLAMA_MODEL: str = "qwen2.5:7b"
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    # Database
    DATABASE_URL: str = "sqlite:///./elida.db"
    
    # JWT Authentication
    JWT_SECRET: str = "dev-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    model_config = {"env_file": ".env", "extra": "ignore", "case_sensitive": True}

settings = Settings()
