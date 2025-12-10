from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    تنظیمات پروژه
    """
    # پایگاه‌داده
    DATABASE_SERVER: str = "localhost"
    DATABASE_PORT: int = 1433
    DATABASE_NAME: str = "IT_Asset_Management"
    DATABASE_USER: str = "sa"
    DATABASE_PASSWORD: str = "YourPassword123!"
    
    # Active Directory
    AD_SERVER: str = "ldap://your-ad-server. com"
    AD_USERNAME:  str = "admin@yourdomain.com"
    AD_PASSWORD: str = "YourADPassword"
    AD_BASE_DN: str = "dc=yourdomain,dc=com"
    
    # API
    API_TITLE: str = "IT Asset Management API"
    API_VERSION: str = "1.0.0"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()
