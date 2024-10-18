from datetime import datetime
from lib2to3.pytree import Base

from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, Boolean

metadata = MetaData()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime)


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("name", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("updated_at", DateTime, nullable=False, default=datetime.utcnow()),
    Column("created_at", DateTime, nullable=False, default=datetime),
    Column("is_active", Boolean, default=False),
    Column("is_admin", Boolean, default=False),
)
