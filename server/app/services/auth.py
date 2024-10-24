from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, SubscriptionSummary

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_user(self, user_create: UserCreate):
        existing_user = self.user_repository.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with that email already"
            )
        user = User(
            name=user_create.name,
            email=user_create.email,
            hashed_password=self.get_password_hash(user_create.password)
        )
        return self.user_repository.create_user(user)

    def get_profile(self, user_id: int = None, user_name: str = None):
        if user_id:
            user = self.user_repository.get_user_by_id(user_id)
        elif user_name:
            user = self.user_repository.get_user_by_name(user_name)
        else:
            raise HTTPException(status_code=400, detail="User ID or name must be provided")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        subscriptions = self.user_repository.get_subscriptions(user.id)
        subscribers = self.user_repository.get_subscribers(user.id)

        user_response = UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            subscriptions=[SubscriptionSummary(id=sub.id, name=sub.name, email=sub.email) for sub in subscriptions],
            subscribers=[SubscriptionSummary(id=sub.id, name=sub.name, email=sub.email) for sub in subscribers],
        )
        return user_response

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
