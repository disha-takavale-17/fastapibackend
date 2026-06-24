import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models.user import User
# from app.database.models.sessions import SessionModel
from app.auth import  verify_password

SECRET_KEY = "your-secret-key"  # use env var in production
ALGORITHM = "HS256"


def create_access_token(user_id: str, expires_delta: timedelta = None):
    if expires_delta is None:
        expires_delta = timedelta(hours=24)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(prefix="/users", tags=["Users"])
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(str(user.id))
    return {
        "email": user.email,
        "name": user.name if hasattr(user, "name") else None,
        "access_token": access_token
    }
# router.post("/login")
# def login(username: str, password: str, db: Session):
#     user = db.query(User).filter(User.email == username).first()
#     if not user or not verify_password(password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     session_id = str(uuid.uuid4())
#     expires_at = datetime.utcnow() + timedelta(hours=1)
#     db_session = SessionModel(id=session_id, user_id=user.id, expires_at=expires_at)
#     db.add(db_session)
#     db.commit()
#     return {"session_id": session_id, "user_id": user.id}

# # routes/auth.py
# @router.post("/login")
# async def login_route(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     result = login(form_data.username, form_data.password, db)

#     response = JSONResponse(content={
#         "message": "Login successful",
#         "user_id": result["user_id"],
#         "session_id": result["session_id"]
#     })
#     response.set_cookie(
#         key="sessionId",
#         value=result["session_id"],
#         httponly=True,
#         secure=False,   # True in production
#         samesite="lax",
#         path="/"
#     )
#     return response

