from fastapi import APIRouter, Depends, HTTPException, Response

from app.database.models.user import User
from app.helpers.utility import verify_password
from sqlalchemy.orm import Session
from app.database.database import get_db


from app.schema.user_schema import UserCreate, UserPatch, UserRead
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm
from app.auth import  get_current_user
from app.services.user_services import (
    create_user,
    get_all_users,
    get_all_usernames,
    put_user,
    patch_user,
    delete_user,
)

# security = HTTPBasic()

router = APIRouter(
    prefix="/users",
    tags=["users"],
    
)

# # new
# @router.get("/validate")
# def validate_session(current_user: User = Depends(get_current_user)):
#     # If get_current_user succeeds, session is valid
#     return {"message": "Valid", "user_id": current_user.id}

# # new
# @router.post("/logout")
# def logout(response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     # Delete all sessions for this user
#     db.query(SessionModel).filter(SessionModel.user_id == current_user.id).delete()
#     db.commit()
#     response.delete_cookie("sessionId")
#     return {"message": "Logged out"}

# # new
# @router.post("/re-auth")
# def re_auth(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Verify password again
#     user = db.query(User).filter(User.email == current_user.email).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Re-authentication failed")

#     return {"message": "Re-authenticated"}


@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=list[UserRead])
def get_all_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_users(db)
  

# @router.get("/usernames", response_model=list[str])
# def route_get_all_usernames(db: Session = Depends(get_db)):
#     return get_all_usernames(db)

@router.get("/usernames", response_model=list[str])
def get_all_usernames(
   current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_all_usernames(db)

@router.put("/{user_id}", response_model=UserRead)
def put_user(
    user_id: int,
    updated_user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    db_user = put_user(db, user_id, updated_user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserRead)
def patch_user(user_id: int, user_patch: UserPatch, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = patch_user(db, user_id, user_patch)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# @router.post("/users/logout")
# def logout(response: Response):
#     response.delete_cookie("token")   # remove JWT cookie
#     return {"message": "Logged out"}
