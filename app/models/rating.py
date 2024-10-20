from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.database import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    value = Column(Integer, nullable=False)  # 1 или -1


# ratings = Table(
#     "ratings",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("post_id", Integer, ForeignKey('posts.id'), nullable=False),
#     Column("user_id", Integer, ForeignKey('users.id'), nullable=False),
#     Column("value", Integer, nullable=False)
# )
