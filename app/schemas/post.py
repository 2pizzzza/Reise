from typing import List

from pydantic import BaseModel
from datetime import datetime

from app.schemas.photo import PhotoResponse


class PostBase(BaseModel):
    title: str
    body: str
    is_visible: bool = True


class PostCreate(PostBase):
    country_name: str
    country_name: str
    images: List[str] = []


class Post(PostBase):
    id: int
    created_at: datetime
    author_id: int
    country_name: str

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    country_id: int
    photos: List[PhotoResponse] = []

    class Config:
        orm_mode = True
