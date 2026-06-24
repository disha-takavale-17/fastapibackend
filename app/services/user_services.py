import datetime
# import uuid
# from app.database.models.sessions import SessionModel
from app.helpers.utility import hash_password
from sqlalchemy.orm import Session
from app.database.models.user import User
from app.schema.user_schema import UserCreate, UserPatch
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
# app/routes/user_routes.py
from app.auth import verify_password

# checks user and created a uuid and save in sessions table
def login(email: str, password: str, db: Session):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Just return user info — NextAuth will handle sessions
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

# POST - Create a new user
HTTPException

def create_user(session: Session, user: UserCreate):
    # Check if email already exists
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = hash_password(user.password)

    # Create new user
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_pw
    )

    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        # If anything unexpected happens, raise a generic error
        raise HTTPException(status_code=500, detail="Database error during user creation")

    session.refresh(new_user)
    return new_user

# GET - Get all users (full details)
def get_all_users(session: Session):
    return session.query(User).all()

# GET - Get all usernames only
def get_all_usernames(session: Session):
    return [user.username for user in session.query(User.username).all()]

# PUT - Replace entire user record
def put_user(session: Session, user_id: int, updated_user: UserCreate):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    # overwrite all fields except id
    db_user.username = updated_user.username
    db_user.email = updated_user.email
    db_user.age = updated_user.age
    session.commit()
    session.refresh(db_user)
    return db_user

# PATCH - Update user partially
def patch_user(session: Session, user_id: int, user_patch: UserPatch):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for field, value in user_patch.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    session.commit()
    session.refresh(db_user)
    return db_user

# DELETE - Remove a user
def delete_user(session: Session, user_id: int):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    session.delete(db_user)
    session.commit()
    return db_user
