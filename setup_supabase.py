#!/usr/bin/env python3
"""
Interactive setup script for Supabase configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("🚀 Supabase Setup for Bookstore App")
    print("=" * 50)
    print()

def get_supabase_info():
    """Get Supabase connection details from user"""
    print("📋 Please provide your Supabase connection details:")
    print("(Get these from: Supabase Dashboard > Settings > Database)")
    print()
    
    project_ref = input("🔗 Project Reference (from your Supabase URL): ").strip()
    password = input("🔑 Database Password: ").strip()
    
    if not project_ref or not password:
        print("❌ Both project reference and password are required!")
        return None
    
    # Construct connection string
    database_url = f"postgresql://postgres:{password}@db.{project_ref}.supabase.co:5432/postgres"
    
    print(f"\n✅ Connection string created:")
    print(f"📡 {database_url}")
    
    return database_url

def update_env_file(database_url):
    """Update .env file with Supabase URL"""
    env_file = Path(".env")
    
    # Read existing .env file
    env_content = ""
    if env_file.exists():
        with open(env_file, 'r') as f:
            env_content = f.read()
    
    # Update or add DATABASE_URL
    lines = env_content.split('\n')
    updated = False
    
    for i, line in enumerate(lines):
        if line.startswith("DATABASE_URL="):
            lines[i] = f"DATABASE_URL={database_url}"
            updated = True
            break
    
    if not updated:
        lines.append(f"DATABASE_URL={database_url}")
    
    # Write back to file
    with open(env_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Updated .env file with Supabase connection")

def set_environment_variable(database_url):
    """Set environment variable for current session"""
    try:
        # For PowerShell
        subprocess.run([
            "powershell", "-Command", 
            f"$env:DATABASE_URL='{database_url}'"
        ], check=True)
        print("✅ Environment variable set for current session")
    except:
        print("⚠️  Could not set environment variable automatically")
        print("Please run: set DATABASE_URL=" + database_url)

def test_connection(database_url):
    """Test the database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"🐘 PostgreSQL version: {version}")
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
        print("✅ psycopg2-binary installed")
    except:
        print("⚠️  Could not install psycopg2-binary")
        print("Please run: pip install psycopg2-binary")

def run_migration():
    """Run database migration"""
    print("\n🔄 Running database migration...")
    try:
        subprocess.run([sys.executable, "migrate_to_postgres.py"], check=True)
        print("✅ Migration completed!")
        return True
    except:
        print("❌ Migration failed!")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Get Supabase info
    database_url = get_supabase_info()
    if not database_url:
        return
    
    # Step 2: Update .env file
    update_env_file(database_url)
    
    # Step 3: Set environment variable
    set_environment_variable(database_url)
    
    # Step 4: Install dependencies
    install_dependencies()
    
    # Step 5: Test connection
    if test_connection(database_url):
        print("\n🎉 Supabase setup successful!")
        
        # Ask if user wants to run migration
        run_migration_choice = input("\n🔄 Do you want to run the database migration now? (y/n): ").strip().lower()
        if run_migration_choice in ['y', 'yes']:
            run_migration()
        
        print("\n📝 Next steps:")
        print("1. Test your app: python -c 'import app.main; print(\"✅ App ready!\")'")
        print("2. Start your app: uvicorn app.main:app --reload")
        print("3. Deploy to Vercel: vercel")
        
    else:
        print("\n💥 Setup failed!")
        print("Please check your Supabase connection details and try again.")

if __name__ == "__main__":
    main()
