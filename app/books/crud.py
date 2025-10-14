from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Book
from app.schemas import BookCreate, BookUpdate

def get_book(db: Session, book_id: int) -> Optional[Book]:
    """Get a book by ID"""
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    active_only: bool = True
) -> List[Book]:
    """Get list of books with optional search and pagination"""
    query = db.query(Book)
    
    if active_only:
        query = query.filter(Book.is_active == True)
    
    if search:
        query = query.filter(
            Book.title.ilike(f"%{search}%") | 
            Book.author.ilike(f"%{search}%") |
            Book.description.ilike(f"%{search}%")
        )
    
    return query.offset(skip).limit(limit).all()

def create_book(db: Session, book: BookCreate) -> Book:
    """Create a new book"""
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: BookUpdate) -> Optional[Book]:
    """Update a book"""
    db_book = get_book(db, book_id)
    if not db_book:
        return None
    
    update_data = book.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)
    
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """Delete a book (soft delete by setting is_active=False)"""
    db_book = get_book(db, book_id)
    if not db_book:
        return False
    
    db_book.is_active = False
    db.commit()
    return True

def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    """Get a book by ISBN"""
    return db.query(Book).filter(Book.isbn == isbn).first()

def check_book_stock(db: Session, book_id: int, quantity: int) -> bool:
    """Check if book has sufficient stock"""
    book = get_book(db, book_id)
    if not book or not book.is_active:
        return False
    return book.stock_quantity >= quantity

def update_book_stock(db: Session, book_id: int, quantity_change: int) -> bool:
    """Update book stock quantity"""
    book = get_book(db, book_id)
    if not book:
        return False
    
    book.stock_quantity += quantity_change
    if book.stock_quantity < 0:
        book.stock_quantity = 0
    
    db.commit()
    return True
