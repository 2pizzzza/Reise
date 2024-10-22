import os
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.post import Post, Photo
from app.schemas.post import PostCreate
from app.models.vote import Vote


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: PostCreate, author_id: int, country_id: int) -> Post:
        db_post = Post(**post.dict(exclude={"country_name", "images", "tags"}), author_id=author_id, country_id=country_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)

        for image in post.images:
            self.save_photo(db_post.id, image)

        return db_post

    def get_all_posts(self):
        return self.db.query(Post)
    def save_photo(self, post_id: int, image: UploadFile):
        existing_photos = self.db.query(Photo).filter(Photo.post_id == post_id).count()
        if existing_photos >= 10:
            raise HTTPException(status_code=400, detail="Post can't have more than 10 photos.")

        if image.size > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Each image must be less than 5 MB.")

        image_filename = f"{uuid4()}.jpg"
        image_path = os.path.join("static/media/img", image_filename)

        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())

        photo = Photo(post_id=post_id, image=image_path)
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)

    def update_post(self, post_id: int, post_data: PostCreate) -> Post:
        db_post = self.db.query(Post).filter(Post.id == post_id).first()
        if db_post:
            for key, value in post_data.dict(exclude={"country_name"}).items():
                setattr(db_post, key, value)
            self.db.commit()
            self.db.refresh(db_post)
        return db_post

    def delete_post(self, post_id: int):
        db_post = self.db.query(Post).filter(Post.id == post_id).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
        return db_post

    def get_vote_count(self, post_id: int) -> dict:
        vote_counts = (
            self.db.query(Vote.vote_type, func.count(Vote.id).label("count"))
            .filter(Vote.post_id == post_id)
            .group_by(Vote.vote_type)
            .all()
        )

        return {vote_type: count for vote_type, count in vote_counts}

    def get_post(self, post_id: int) -> Post:
        return (
            self.db.query(Post)
            .options(
                joinedload(Post.photos),
                joinedload(Post.author)
            )
            .filter(Post.id == post_id)
            .first()
        )