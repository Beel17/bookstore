#!/usr/bin/env python3
"""
Test script to verify Supabase PostgreSQL connection
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_connection(database_url):
    """Test database connection"""
    print(f"🔌 Testing connection to Supabase...")
    print(f"📍 Host: {database_url.split('@')[1].split(':')[0] if '@' in database_url else 'Unknown'}")
    
    try:
        # Create engine
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"🐘 PostgreSQL version: {version}")
            
            # Test basic query
            result = connection.execute(text("SELECT current_database(), current_user;"))
            db_info = result.fetchone()
            print(f"📊 Database: {db_info[0]}")
            print(f"👤 User: {db_info[1]}")
            
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Supabase Connection Test")
    print("=" * 40)
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("\n📝 To set it, run:")
        print("set DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres")
        print("\n🔗 Get your connection string from:")
        print("Supabase Dashboard > Settings > Database > Connection string > URI")
        return
    
    if not database_url.startswith("postgresql://"):
        print("❌ DATABASE_URL must be a PostgreSQL connection string!")
        print("Expected format: postgresql://user:password@host:port/database")
        return
    
    # Test connection
    if test_connection(database_url):
        print("\n🎉 Database connection successful!")
        print("You're ready to run the migration script!")
    else:
        print("\n💥 Database connection failed!")
        print("Please check your connection string and try again.")

if __name__ == "__main__":
    main()
