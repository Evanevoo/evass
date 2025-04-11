from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gas Cylinder Tracking System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///gas_tracker.db"  # SQLite database in the current directory
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security Configuration
    VERIFY_EMAIL: bool = True
    RESET_TOKEN_EXPIRE_HOURS: int = 48
    MAX_LOGIN_ATTEMPTS: int = 5
    SESSION_TIMEOUT_MINUTES: int = 60
    REQUIRE_2FA: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings() 