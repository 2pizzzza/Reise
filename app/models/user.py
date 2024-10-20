from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    can_post = Column(Boolean, default=True)

    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    ratings = relationship('Rating', back_populates='user')
    subscriptions = relationship('Subscription', back_populates='user')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='subscriptions')
    target_user = relationship('User', foreign_keys=[target_user_id])


# users = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False, unique=True),
#     Column("name", String, nullable=False),
#     Column("hashed_password", String, nullable=False),
#     Column("is_active", Boolean, default=False),
#     Column("is_admin", Boolean, default=False),
#     Column("can_post", Boolean, default=True)
# )
#
# subscriptions = Table(
#     "subscriptions",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", Integer, ForeignKey('users.id'), nullable=False),
#     Column("target_user_id", Integer, ForeignKey('users.id'), nullable=True),
#     Column("country_id", Integer, ForeignKey('countries.id'), nullable=True),
#     Column("tag_id", Integer, ForeignKey('tags.id'), nullable=True)
# )
