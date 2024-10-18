from fastapi import HTTPException, status

from app.core.security import verify_password, create_access_token, get_password_hash
from app.schemas.user import UserCreate
from app.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_service.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def create_user(self, user: UserCreate):
        existing_user = await self.user_service.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        return await self.user_service.create_user(user, hashed_password)

    def create_access_token(self, data: dict):
        return create_access_token(data)
