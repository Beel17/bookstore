"""
Vercel-specific configuration for the bookstore app.
This handles the differences between local development and Vercel deployment.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VercelSettings:
    # Database - Use environment variable from Vercel
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./bookstore.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Paystack
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "")
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    
    # Vercel-specific settings
    IS_VERCEL: bool = os.getenv("VERCEL") == "1"

vercel_settings = VercelSettings()
