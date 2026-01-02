from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Financial Decision Support System"
    API_V1_STR: str = "/api/v1"
    
    # Placeholder for API Keys
    OPENAI_API_KEY: str = ""
    FRED_API_KEY: str = ""
    GEMINI_API_KEY: Optional[str] = None
    
    LLM_PROVIDER: str = "auto"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    OLLAMA_MODEL: str = "llama3.1:latest"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
