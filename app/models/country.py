from sqlalchemy import Column, Integer, String, Table

from app.db.database import Base


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    posts = relationship('Post', back_populates='country')
    subscriptions = relationship('Subscription', back_populates='country')


# countries = Table(
#     "countries",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, unique=True),
# )
