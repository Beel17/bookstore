from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import Book, BookCreate, BookUpdate
from app.books.crud import (
    get_books, get_book, create_book, update_book, 
    delete_book, get_book_by_isbn
)
from app.auth.utils import get_current_active_user, get_current_admin_user

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of books with optional search and pagination"""
    books = get_books(db, skip=skip, limit=limit, search=search)
    return books

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID"""
    book = get_book(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Book not found"
        )
    return book

@router.post("/", response_model=Book)
def create_new_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new book (admin only)"""
    # Check if ISBN already exists
    if book.isbn:
        existing_book = get_book_by_isbn(db, book.isbn)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    return create_book(db=db, book=book)

@router.put("/{book_id}", response_model=Book)
def update_existing_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update a book (admin only)"""
    # Check if ISBN already exists (if being updated)
    if book.isbn:
        existing_book = get_book_by_isbn(db, book.isbn)
        if existing_book and existing_book.id != book_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ISBN already exists"
            )
    
    db_book = update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book

@router.delete("/{book_id}")
def delete_existing_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a book (admin only)"""
    success = delete_book(db=db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return {"message": "Book deleted successfully"}

@router.get("/isbn/{isbn}", response_model=Book)
def read_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    """Get a book by ISBN"""
    book = get_book_by_isbn(db, isbn=isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book
