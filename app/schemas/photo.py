from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class PhotoCreate(BaseModel):
    image: UploadFile

class PhotoResponse(PhotoCreate):
    id: int
    image: str

    class Config:
        orm_mode = True
