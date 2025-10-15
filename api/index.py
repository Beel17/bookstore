"""
Vercel serverless function entry point for FastAPI bookstore app.
"""
import sys
import os
from pathlib import Path

# Add the parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Set environment variables for Vercel
os.environ.setdefault("ENVIRONMENT", "production")

try:
    # Import and configure the app
    from app.main import app
    
    # This is the ASGI application that Vercel will use
    handler = app
    
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Try alternative import
    try:
        from app.config import settings
        print(f"Settings loaded: DATABASE_URL = {settings.DATABASE_URL[:50]}...")
    except Exception as e2:
        print(f"Settings import also failed: {e2}")
    
    raise
except Exception as e:
    print(f"Unexpected error: {e}")
    raise
