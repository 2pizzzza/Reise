from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base


class VoteType(enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"

class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    vote_type = Column(Enum(VoteType), nullable=False)

    post = relationship("Post", back_populates="votes")
    user = relationship("User", back_populates="votes")
