from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    async def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    async def create_user(self, user: UserCreate, hashed_password: str):
        return self.user_repository.create_user(user, hashed_password)

    async def update_user(self, user_id: int, user_update: UserUpdate):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return None
        return self.user_repository.update_user(user, user_update)
