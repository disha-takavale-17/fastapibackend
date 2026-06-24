from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    

class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    

class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None

class UserRead(UserBase):
    model_config = {"from_attributes": True}
    id: int
