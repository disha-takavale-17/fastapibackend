from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.models.user import User
from app.database.models.book import Book
from app.schema.book_schema import BookCreate, BookRead
import random

# Get all active books with ownership info
def get_books_list(db, current_user):
    books = db.query(Book).filter(Book.is_active == True).all()
    return [
        BookRead(
            id=book.id,
            title=book.title,
            author=book.author,
            published_year=book.published_year,
            is_active=book.is_active,
            user_id=book.user_id,
            status="Mine" if book.user_id == current_user.id else "Available"
        )
        for book in books
    ]


# Create a new book
def create_book(book: BookCreate, db: Session):
    existing = db.query(Book).filter(
        Book.title == book.title,
        Book.is_active == True
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="This book already exists")

    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
