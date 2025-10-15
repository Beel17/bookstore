#!/usr/bin/env python3
"""
Database migration script for moving from SQLite to PostgreSQL
Run this script to set up your PostgreSQL database with the same data as SQLite
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Book, Order, OrderItem, Payment, UserRole
from app.auth.utils import get_password_hash
from app.config import settings

def create_postgres_tables(postgres_url):
    """Create all tables in PostgreSQL database"""
    print("🔧 Creating PostgreSQL tables...")
    
    # Create engine
    engine = create_engine(postgres_url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def migrate_sqlite_data(postgres_url):
    """Migrate data from SQLite to PostgreSQL"""
    print("📦 Migrating data from SQLite to PostgreSQL...")
    
    # Connect to both databases
    sqlite_url = "sqlite:///./bookstore.db"
    sqlite_engine = create_engine(sqlite_url)
    postgres_engine = create_engine(postgres_url)
    
    sqlite_session = sessionmaker(bind=sqlite_engine)()
    postgres_session = sessionmaker(bind=postgres_engine)()
    
    try:
        # Migrate Users
        print("👥 Migrating users...")
        users = sqlite_session.query(User).all()
        for user in users:
            # Create new user in PostgreSQL
            new_user = User(
                id=user.id,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            postgres_session.add(new_user)
        
        # Migrate Books
        print("📚 Migrating books...")
        books = sqlite_session.query(Book).all()
        for book in books:
            new_book = Book(
                id=book.id,
                title=book.title,
                author=book.author,
                description=book.description,
                price=book.price,
                stock_quantity=book.stock_quantity,
                image_url=book.image_url,
                created_at=book.created_at,
                updated_at=book.updated_at
            )
            postgres_session.add(new_book)
        
        # Migrate Orders
        print("📦 Migrating orders...")
        orders = sqlite_session.query(Order).all()
        for order in orders:
            new_order = Order(
                id=order.id,
                user_id=order.user_id,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at
            )
            postgres_session.add(new_order)
        
        # Migrate Order Items
        print("🛒 Migrating order items...")
        order_items = sqlite_session.query(OrderItem).all()
        for item in order_items:
            new_item = OrderItem(
                id=item.id,
                order_id=item.order_id,
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.price
            )
            postgres_session.add(new_item)
        
        # Commit all changes
        postgres_session.commit()
        print("✅ Data migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        postgres_session.rollback()
        raise
    finally:
        sqlite_session.close()
        postgres_session.close()

def create_sample_data(postgres_url):
    """Create sample data in PostgreSQL database"""
    print("🎨 Creating sample data...")
    
    engine = create_engine(postgres_url)
    session = sessionmaker(bind=engine)()
    
    try:
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@bookstore.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            is_active=True
        )
        session.add(admin_user)
        
        # Create sample books
        sample_books = [
            Book(
                title="Python Programming",
                author="John Doe",
                description="Learn Python from scratch with practical examples.",
                price=29.99,
                stock_quantity=50,
                image_url="/static/images/python-book.svg"
            ),
            Book(
                title="FastAPI Development",
                author="Jane Smith",
                description="Build modern APIs with FastAPI and Python.",
                price=39.99,
                stock_quantity=30,
                image_url="/static/images/fastapi-book.svg"
            ),
            Book(
                title="React Fundamentals",
                author="Bob Johnson",
                description="Master React development with hooks and modern patterns.",
                price=34.99,
                stock_quantity=40,
                image_url="/static/images/react-book.svg"
            ),
            Book(
                title="Database Design",
                author="Alice Brown",
                description="Learn database design principles and best practices.",
                price=24.99,
                stock_quantity=25,
                image_url="/static/images/database-book.svg"
            ),
            Book(
                title="Docker & DevOps",
                author="Charlie Wilson",
                description="Containerization and deployment strategies.",
                price=44.99,
                stock_quantity=20,
                image_url="/static/images/docker-book.svg"
            )
        ]
        
        for book in sample_books:
            session.add(book)
        
        session.commit()
        print("✅ Sample data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        session.rollback()
        raise
    finally:
        session.close()

def main():
    """Main migration function"""
    print("🚀 PostgreSQL Migration Script")
    print("=" * 40)
    
    # Get PostgreSQL URL from environment or prompt
    postgres_url = os.getenv("DATABASE_URL")
    
    if not postgres_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("Please set it to your PostgreSQL connection string:")
        print("Example: postgresql://user:password@host:5432/database")
        return
    
    if not postgres_url.startswith("postgresql://"):
        print("❌ DATABASE_URL must be a PostgreSQL connection string!")
        return
    
    print(f"📡 Connecting to: {postgres_url.split('@')[1] if '@' in postgres_url else 'PostgreSQL database'}")
    
    try:
        # Step 1: Create tables
        create_postgres_tables(postgres_url)
        
        # Step 2: Check if SQLite database exists
        if os.path.exists("bookstore.db"):
            print("\n📁 SQLite database found. Migrating data...")
            migrate_sqlite_data(postgres_url)
        else:
            print("\n📁 No SQLite database found. Creating sample data...")
            create_sample_data(postgres_url)
        
        print("\n🎉 Migration completed successfully!")
        print("You can now deploy to Vercel with your PostgreSQL database.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
