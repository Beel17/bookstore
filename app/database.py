from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL environment variable is required!")

# Create database engine with proper connection pooling for production
if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url, 
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration optimized for Vercel serverless
    engine = create_engine(
        database_url,
        pool_size=5,  # Smaller pool for serverless
        max_overflow=10,  # Reduced overflow for serverless
        pool_pre_ping=True,  # Test connections before use
        pool_recycle=300,  # Recycle connections every 5 minutes
        connect_args={
            "connect_timeout": 10,  # 10 second connection timeout
            "options": "-c timezone=utc"  # Set timezone to UTC
        }
    )
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()