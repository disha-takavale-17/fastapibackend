from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer)
    # image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="books")

    __table_args__ = (
        UniqueConstraint("title", name="uq_book_title"),  # prevent duplicate titles
    )
