from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.database.models.book import Book
from app.database.models.user import User
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.book_schema import BookCreate, BookRead
from app.services import book_services
import random
from ..utils.cache import get_cache, set_cache, increment_popularity, get_top_books
from sqlalchemy import func

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    # dependencies=[Depends(get_current_user)]
)
sample_images =[
        "https://picsum.photos/200/300?random=1",
        "https://picsum.photos/200/300?random=2",
        "https://picsum.photos/200/300?random=3",
        "https://placekitten.com/200/300",
        "https://dummyimage.com/200x300/000/fff&text=Book",
        "https://picsum.photos/200/300?random=4",
    ]
# 1. Get all books list
# @router.get("/", response_model=list[BookRead])
# def get_books_list(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     return book_services.get_books_list(db, current_user)

@router.get("/", response_model=list[BookRead])
def get_books_list_public(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/title/{title}", response_model=BookRead)
def get_book_by_title(title: str, db: Session = Depends(get_db)):
    key = f"book:{title.lower()}"

    # 1. Check cache first
    cached = get_cache(key)
    if cached:
        return cached

    # 2. Query DB
    book = db.query(Book).filter(func.lower(Book.title) == title.lower()).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book_dict = BookRead.from_orm(book).dict()

    # 3. Track popularity
    increment_popularity(title)

    # 4. Cache only if in top 10
    top_books = get_top_books(10)  # already strings because decode_responses=True
    if title.lower() in top_books:
        set_cache(key, book_dict, ttl=600)

    # 5. Return the book dict
    return book_dict


# 2. Create a new book
@router.post("/create-book", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_services.create_book(book, db)

# # 3. Update entire book (PUT)
# @router.put("/{book_id}", response_model=BookRead)
# def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
#     return book_services.update_book(book_id, book, db)

# # 4. Partially update book (PATCH)
# @router.patch("/{book_id}", response_model=BookRead)
# def patch_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
#     return book_services.patch_book(book_id, book, db)

# # 5. Soft delete book
# @router.delete("/{book_id}")
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     return book_services.delete_book(book_id, db)
