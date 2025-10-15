from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create database engine
database_url = settings.DATABASE_URL

if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set!")

if database_url.startswith("sqlite"):
    engine = create_engine(
        database_url, 
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(database_url)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()