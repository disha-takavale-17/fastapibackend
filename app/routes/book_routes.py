from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.database.models.user import User
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.book_schema import BookCreate, BookRead
from app.services import book_services

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)]
)

# 1. Get all books list
@router.get("/", response_model=list[BookRead])
def get_books_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return book_services.get_books_list(db, current_user)

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
