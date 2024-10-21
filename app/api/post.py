from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas.post import PostCreate, Post, PostResponse
from app.repositories.post_repository import PostRepository
from app.db.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.services.post import PostService

router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
    country_name: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post_data = PostCreate(
        title=title,
        body=body,
        country_name=country_name,
        images=images
    )

    post_service = PostService(db)
    db_post = post_service.create_post(post_data, author_id=current_user.id)

    return {
        "id": db_post.id,
        "title": db_post.title,
        "body": db_post.body,
        "author_id": db_post.author_id,
        "created_at": db_post.created_at,
        "is_visible": db_post.is_visible,
        "country_name": db_post.country.name
    }


@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post_service = PostService(db)
    post = post_service.get_post(post_id)
    return post


@router.put("/posts/{post_id}")
def update_post(post_id: int, post: PostCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    post_service = PostService(db)
    db_post = post_service.update_post(post_id, post)
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return db_post


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_service = PostService(db)
    message = post_service.delete_post(post_id)
    return {"message": message}
