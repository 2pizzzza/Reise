from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    target_user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=True)

    user = relationship('User', foreign_keys=[user_id], back_populates='subscriptions')
    target_user = relationship('User', foreign_keys=[target_user_id])


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
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")

    subscriptions = relationship('Subscription', foreign_keys=[Subscription.user_id], back_populates='user',
                                 cascade="all, delete-orphan")
    subscribers = relationship('Subscription', foreign_keys=[Subscription.target_user_id], back_populates='target_user',
                               cascade="all, delete-orphan")
