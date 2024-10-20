from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Table
from datetime import datetime
from app.db.database import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# comments = Table(
#     "comments",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("post_id", Integer, ForeignKey('posts.id'), nullable=False),
#     Column("user_id", Integer, ForeignKey('users.id'), nullable=False),
#     Column("text", Text, nullable=False),
#     Column("created_at", DateTime, default=datetime.utcnow)
# )
