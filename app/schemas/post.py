from typing import List

from fastapi import UploadFile
from pydantic import BaseModel
from datetime import datetime

from app.schemas.photo import PhotoResponse


class PostBase(BaseModel):
    title: str
    body: str
    is_visible: bool = True


class PostCreate(BaseModel):
    title: str
    body: str
    country_name: str
    images: List[UploadFile]


class Post(PostBase):
    id: int
    created_at: datetime
    author_id: int
    country_name: str

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    is_visible: bool
    created_at: datetime
    author_id: int
    photos: List[PhotoResponse]

    class Config:
        orm_mode = True