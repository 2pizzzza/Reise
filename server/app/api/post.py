from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.comment import CommentResponse, CommentCreate
from app.schemas.post import PostCreate, Post, PostResponse
from app.services.comment import CommentService
from app.services.post import PostService
from app.services.vote import VoteService

router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(
        title: str = Form(...),
        body: str = Form(...),
        country_name: str = Form(...),
        tags: str = Form(...),
        images: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]

    post_data = PostCreate(
        title=title,
        body=body,
        country_name=country_name,
        images=images,
        tags=tag_list
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
        "tags": [tag.name for tag in db_post.tags],
        "country_name": db_post.country.name,
        "photos": [{"id": photo.id, "url": f"/static/media/img/{photo.image}"} for photo in db_post.photos]
    }


@router.get("/{user_id}/posts/", response_model=List[PostResponse])
async def get_user_photos(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_service = PostService(db)
    photos = post_service.get_all_post_by_user(user_id)
    return photos


@router.get("/posts/", response_model=List[PostResponse])
async def get_all_posts(db: Session = Depends(get_db)):
    post_service = PostService(db)
    posts = post_service.get_all_posts()
    return posts


@router.get("/posts/{post_id}")
def read_post(post_id: int, db: Session = Depends(get_db)):
    post_service = PostService(db)
    post = post_service.get_post(post_id)

    vote_counts = post_service.get_post_vote_counts(post_id)

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "author_name": post.author.name,
        "created_at": post.created_at,
        "is_visible": post.is_visible,
        "country_name": post.country.name,
        "tag": post.tags,
        "photos": post.photos,
        "vote_counts": vote_counts,
    }


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


@router.post("/{post_id}/comments", response_model=CommentResponse)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    comment_service = CommentService(db)
    new_comment = comment_service.create_comment(post_id, current_user.id, comment.content)
    return new_comment


@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    comments = comment_service.get_comments_by_post(post_id)
    return comments


@router.post("/{post_id}/upvote")
def upvote_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vote_service = VoteService(db)
    rating_change = vote_service.upvote(post_id, current_user.id)
    return {"rating_change": rating_change}


@router.post("/{post_id}/downvote")
def downvote_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vote_service = VoteService(db)
    rating_change = vote_service.downvote(post_id, current_user.id)
    return {"rating_change": rating_change}
