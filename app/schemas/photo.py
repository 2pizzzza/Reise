from pydantic import BaseModel
from typing import Optional


class PhotoCreate(BaseModel):
    image: str


class PhotoResponse(PhotoCreate):
    id: int
    post_id: int

    class Config:
        orm_mode = True
