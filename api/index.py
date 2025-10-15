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

# Set environment for Vercel
os.environ.setdefault("ENVIRONMENT", "production")

# Import the FastAPI app
from app.main import app

# This is the ASGI application that Vercel will use
handler = app
