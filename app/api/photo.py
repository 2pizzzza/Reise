from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

IMAGE_DIRECTORY = "static/media/img"


@router.get("/images/{image_name}")
def get_image(image_name: str):
    image_path = os.path.join(IMAGE_DIRECTORY, image_name)

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)