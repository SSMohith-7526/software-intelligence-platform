import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application Config
    APP_NAME: str = "AI_OS_Master_Control"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # LLM Config
    # Defaulting to localhost:11434 for local Ollama execution
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # We use qwen2.5-coder or llama3 as they are highly optimized for AST/code comprehension
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5-coder") 
    
    # Workspace Config
    UPLOAD_DIRECTORY: str = os.getenv("UPLOAD_DIRECTORY", "./workspace/sandbox")
    MAX_FILE_SIZE_MB: int = 15

    class Config:
        env_file = ".env"

# Global instance imported by agents
settings = Settings()

# Alias for direct imports in legacy files
OLLAMA_BASE_URL = settings.OLLAMA_BASE_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL