from pydantic import BaseModel, RootModel
from typing import Optional


    
class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int
    user_id: int

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    is_active: bool
    user_id: Optional[int]
    image_url: Optional[str]= None

    model_config = {"from_attributes": True}
