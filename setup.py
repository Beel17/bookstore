#!/usr/bin/env python3
"""
Setup script for the Bookstore application.
This script helps with initial database setup and admin user creation.
"""

import os
import sys
import asyncio
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, User, UserRole
from app.auth.utils import get_password_hash
from app.config import settings

def create_tables():
    """Create database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def create_admin_user():
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@bookstore.com").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = User(
            email="admin@bookstore.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin@bookstore.com")
        print("Password: admin123")
        print("Please change the admin password after first login!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_books():
    """Create sample books for testing"""
    from app.books.crud import create_book
    from app.schemas import BookCreate
    
    db = SessionLocal()
    try:
        # Check if books already exist
        from app.models import Book
        existing_books = db.query(Book).count()
        if existing_books > 0:
            print("Books already exist in database!")
            return
        
        sample_books = [
            {
                "title": "Python Programming",
                "author": "Guido van Rossum",
                "description": "Learn Python programming from the creator of Python. This comprehensive guide covers everything from basic syntax to advanced concepts like decorators, generators, and async programming.",
                "price": 49.99,
                "stock_quantity": 50,
                "isbn": "978-0134076430",
                "image_url": "/static/images/python-book.svg"
            },
            {
                "title": "FastAPI Cookbook",
                "author": "Sebastian Ramirez",
                "description": "Master FastAPI development with practical recipes. Learn to build high-performance APIs with automatic documentation, type hints, and modern Python features.",
                "price": 39.99,
                "stock_quantity": 30,
                "isbn": "978-0134076431",
                "image_url": "/static/images/fastapi-book.svg"
            },
            {
                "title": "Web Development with React",
                "author": "Facebook Team",
                "description": "Build modern web applications with React. Learn component-based architecture, hooks, state management, and best practices for scalable frontend development.",
                "price": 59.99,
                "stock_quantity": 25,
                "isbn": "978-0134076432",
                "image_url": "/static/images/react-book.svg"
            },
            {
                "title": "Database Design",
                "author": "Database Expert",
                "description": "Learn database design principles and best practices. Master SQL, normalization, indexing, and both relational and NoSQL database architectures.",
                "price": 44.99,
                "stock_quantity": 20,
                "isbn": "978-0134076433",
                "image_url": "/static/images/database-book.svg"
            },
            {
                "title": "Docker for Developers",
                "author": "Container Expert",
                "description": "Master containerization with Docker. Learn to containerize applications, manage multi-container setups, and deploy with Docker Compose and orchestration tools.",
                "price": 34.99,
                "stock_quantity": 15,
                "isbn": "978-0134076434",
                "image_url": "/static/images/docker-book.svg"
            }
        ]
        
        for book_data in sample_books:
            book_create = BookCreate(**book_data)
            create_book(db, book_create)
        
        print("Sample books created successfully!")
        print(f"Added {len(sample_books)} books to the database")
        
    except Exception as e:
        print(f"Error creating sample books: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main setup function"""
    print("Setting up Bookstore Application...")
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print("-" * 50)
    
    # Create tables
    create_tables()
    
    # Create admin user
    create_admin_user()
    
    # Create sample books
    create_sample_books()
    
    print("-" * 50)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the application: uvicorn app.main:app --reload")
    print("2. Visit: http://localhost:8000")
    print("3. Login as admin: admin@bookstore.com / admin123")
    print("4. View API docs: http://localhost:8000/docs")
    print("\nRemember to change the admin password!")

if __name__ == "__main__":
    main()
