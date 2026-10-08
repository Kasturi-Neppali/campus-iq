import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CampusIQ – College Academic Intelligence & Student Success Platform"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "campusiq_super_secret_jwt_key_2026_placement_ready")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    # Default to SQLite local file, override with PostgreSQL in production
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')), 'campusIQ.db')}"
    )
    
    # AI / LLM Integration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
