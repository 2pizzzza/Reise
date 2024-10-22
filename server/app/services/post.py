from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, subqueryload, joinedload
from starlette import status

from app.repositories.post import PostRepository
from app.repositories.country import CountryRepository
from app.schemas.post import PostCreate
from app.schemas.country import CountryCreate
from app.models.post import Post
from app.repositories.user import UserRepository
from app.repositories.tag import TagRepository
from app.models.vote import Vote, VoteType


class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.post_repository = PostRepository(db)
        self.country_repository = CountryRepository(db)
        self.tag_repository = TagRepository(db)

    def create_post(self, post: PostCreate, author_id: int) -> Post:
        user = self.user_repository.get_user_by_id(author_id)
        if not user.can_post:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to create a post")

        country = self.country_repository.get_country_by_name(post.country_name)
        if country is None:
            country = self.country_repository.create_country(CountryCreate(name=post.country_name))

        db_post = self.post_repository.create_post(post, author_id=author_id, country_id=country.id)

        for tag_name in post.tags:
            tag = self.tag_repository.get_or_create_tag(tag_name)
            db_post.tags.append(tag)

        self.db.commit()
        self.db.refresh(db_post)

        return db_post

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

    def get_post_vote_counts(self, post_id: int) -> dict:
        return self.post_repository.get_vote_count(post_id)

    def get_vote_count(self, post_id: int) -> int:
        return self.db.query(func.count(Vote.id)).filter(Vote.post_id == post_id).scalar() or 0

    def get_all_posts(self):
        return ((self.db.query(Post)
                 .filter(Post.is_visible == True))
                .options(
            subqueryload(Post.tags),
            subqueryload(Post.photos),
            joinedload(Post.author)
        ).all())

    def get_post(self, post_id: int):
        post = self.post_repository.get_post(post_id)
        if post is None or (not post.is_visible):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return self.post_repository.get_post(post_id)

    def get_all_post_by_user(self, user_id: int):
        return ((self.db.query(Post)
                 .filter(Post.is_visible == True, Post.author_id == user_id))
                .options(
            subqueryload(Post.tags),
            subqueryload(Post.photos),
            joinedload(Post.author)
        ).all())
