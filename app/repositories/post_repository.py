from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post: PostCreate, author_id: int, country_id: int) -> Post:
        db_post = Post(**post.dict(exclude={"country_name"}), author_id=author_id, country_id=country_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        return db_post

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

    def get_post(self, post_id: int) -> Post:
        return self.db.query(Post).filter(Post.id == post_id).first()
