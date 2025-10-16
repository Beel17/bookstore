#!/usr/bin/env python3
"""
Database seeding script for bookstore
Run this script to populate the database with sample data
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Book, User, UserRole, Base
from app.auth.utils import get_password_hash

def seed_database():
    """Seed the database with sample data"""
    # Use environment variable or default
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not set!")
        return False
    
    try:
        # Create engine and session
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
        
        # Create admin user
        admin = db.query(User).filter(User.email == "admin@bookstore.com").first()
        if not admin:
            admin = User(
                email="admin@bookstore.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            print("✅ Admin user created")
        else:
            print("✅ Admin user already exists")
        
        # Create sample books
        sample_books = [
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": "A classic American novel set in the Jazz Age, following the mysterious Jay Gatsby and his obsession with the beautiful Daisy Buchanan.",
                "price": 15.99,
                "stock_quantity": 50,
                "isbn": "978-0743273565",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "description": "A gripping tale of justice, racial inequality, and childhood innocence in the American South.",
                "price": 14.99,
                "stock_quantity": 40,
                "isbn": "978-0061120084",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "description": "A dystopian social science fiction novel about totalitarian control and surveillance.",
                "price": 13.99,
                "stock_quantity": 60,
                "isbn": "978-0451524935",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "description": "A romantic novel of manners that critiques the British landed gentry at the turn of the 19th century.",
                "price": 12.99,
                "stock_quantity": 35,
                "isbn": "978-0141439518",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "description": "A coming-of-age story following teenager Holden Caulfield's experiences in New York City.",
                "price": 11.99,
                "stock_quantity": 45,
                "isbn": "978-0316769174",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "description": "The first book in the magical Harry Potter series following a young wizard's adventures.",
                "price": 16.99,
                "stock_quantity": 100,
                "isbn": "978-0747532699",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "description": "An epic high-fantasy novel about the quest to destroy the One Ring.",
                "price": 18.99,
                "stock_quantity": 30,
                "isbn": "978-0544003415",
                "image_url": "/static/images/default-book.svg"
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "description": "A science fiction epic set on the desert planet Arrakis, focusing on politics, religion, and ecology.",
                "price": 17.99,
                "stock_quantity": 25,
                "isbn": "978-0441013593",
                "image_url": "/static/images/default-book.svg"
            }
        ]
        
        books_added = 0
        for book_data in sample_books:
            existing = db.query(Book).filter(Book.isbn == book_data["isbn"]).first()
            if not existing:
                book = Book(**book_data)
                db.add(book)
                books_added += 1
                print(f"✅ Added: {book_data['title']}")
            else:
                print(f"⚠️  Already exists: {book_data['title']}")
        
        # Commit all changes
        db.commit()
        
        print(f"\n🎉 Database seeded successfully!")
        print(f"📚 Added {books_added} new books")
        print(f"👤 Admin user: admin@bookstore.com (password: admin123)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🌱 Starting database seeding...")
    success = seed_database()
    if success:
        print("✅ Seeding completed successfully!")
    else:
        print("❌ Seeding failed!")
        exit(1)
