from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.db.database import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship('Post', back_populates='country')
    # subscriptions = relationship('Subscription', back_populates='country')
