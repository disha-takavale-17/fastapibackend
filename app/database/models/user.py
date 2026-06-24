from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    username = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=True)
    first_name= Column(String, nullable=True)
    last_name= Column(String, nullable=True)
    

    books = relationship("Book", back_populates="user")

