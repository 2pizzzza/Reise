from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.repositories.post_repository import PostRepository
from app.repositories.country_repository import CountryRepository
from app.schemas.post import PostCreate
from app.schemas.country import CountryCreate
from app.models.post import Post
from app.repositories.user_repository import UserRepository


class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.post_repository = PostRepository(db)
        self.country_repository = CountryRepository(db)

    def create_post(self, post: PostCreate, author_id: int) -> Post:
        user = self.user_repository.get_user_by_id(author_id)
        if not user.can_post:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to create a post"
            )
        country = self.country_repository.get_country_by_name(post.country_name)
        if country is None:
            country = self.country_repository.create_country(CountryCreate(name=post.country_name))

        return self.post_repository.create_post(post, author_id=author_id, country_id=country.id)

    def update_post(self, post_id: int, post_data: PostCreate):
        return self.post_repository.update_post(post_id, post_data)

    def delete_post(self, post_id: int):
        db_post = self.post_repository.delete_post(post_id)
        if db_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return "Post deleted"

    def get_post(self, post_id: int):
        post = self.post_repository.get_post(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return self.post_repository.get_post(post_id)
