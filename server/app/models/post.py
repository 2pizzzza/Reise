from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_visible = Column(Boolean, default=True)

    author = relationship('User', back_populates='posts')
    country = relationship('Country', back_populates='posts')
    photos = relationship('Photo', back_populates='post', cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary='post_tags', back_populates="posts")


class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    image = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship('Post', back_populates='photos')


class PostTag(Base):
    __tablename__ = 'post_tags'

    post_id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    posts = relationship("Post", secondary='post_tags', back_populates='tags')
