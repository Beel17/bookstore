#!/usr/bin/env python3
"""
Test script to simulate Vercel function locally
"""
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports that the Vercel function needs"""
    print("🧪 Testing imports...")
    
    try:
        print("📦 Testing basic imports...")
        import fastapi
        import uvicorn
        import sqlalchemy
        import jose
        import passlib
        import pydantic
        import jinja2
        import aiofiles
        print("✅ Basic imports successful")
        
        print("📦 Testing app imports...")
        from app.config import settings
        from app.database import engine, SessionLocal
        from app.models import Base, User, Book
        from app.auth.utils import create_access_token
        print("✅ App imports successful")
        
        print("📦 Testing main app...")
        from app.main import app
        print("✅ Main app import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from app.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_app_startup():
    """Test app startup"""
    print("\n🚀 Testing app startup...")
    
    try:
        from app.main import app
        
        # Test if app can be created
        print(f"✅ App created: {app.title}")
        print(f"✅ App version: {app.version}")
        
        # Test routes
        routes = [route.path for route in app.routes]
        print(f"✅ Routes loaded: {len(routes)} routes")
        
        return True
        
    except Exception as e:
        print(f"❌ App startup failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Vercel Function Test")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n💥 Import tests failed!")
        return False
    
    # Test database
    if not test_database_connection():
        print("\n💥 Database tests failed!")
        return False
    
    # Test app startup
    if not test_app_startup():
        print("\n💥 App startup tests failed!")
        return False
    
    print("\n🎉 All tests passed! Your app should work on Vercel.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
