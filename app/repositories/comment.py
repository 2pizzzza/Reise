from typing import List

from sqlalchemy.orm import Session

from app.models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_comment(self, post_id: int, author_id: int, content: str) -> Comment:
        comment = Comment(post_id=post_id, author_id=author_id, content=content)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_comments_by_post(self, post_id: int) -> List[Comment]:
        return self.db.query(Comment).filter(Comment.post_id == post_id).all()
