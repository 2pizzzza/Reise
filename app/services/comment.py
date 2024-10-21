from typing import List

from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repositories.comment import CommentRepository


class CommentService:
    def __init__(self, db: Session):
        self.comment_repository = CommentRepository(db)

    def create_comment(self, post_id: int, author_id: int, content: str) -> Comment:
        return self.comment_repository.create_comment(post_id, author_id, content)

    def get_comments_by_post(self, post_id: int) -> List[Comment]:
        return self.comment_repository.get_comments_by_post(post_id)
