import os
import sys
from dotenv import load_dotenv

# Only load .env in development
if os.getenv("ENVIRONMENT") != "production":
    load_dotenv()

class Settings:
    # Database - REQUIRED for production
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL environment variable is required!")
        print("Please set DATABASE_URL in your Vercel environment variables.")
        sys.exit(1)
    
    # JWT - REQUIRED for production
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    if SECRET_KEY == "your-secret-key-here-change-in-production":
        print("ERROR: SECRET_KEY must be set to a secure value in production!")
        print("Please set SECRET_KEY in your Vercel environment variables.")
        sys.exit(1)
    
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Paystack
    PAYSTACK_SECRET_KEY: str = os.getenv("PAYSTACK_SECRET_KEY", "")
    PAYSTACK_PUBLIC_KEY: str = os.getenv("PAYSTACK_PUBLIC_KEY", "")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")

settings = Settings()
