from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import User, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(user_repository)


@router.get("/profile", response_model=User)
async def read_user_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/updateProfile", response_model=User)
async def update_user_profile(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(get_user_service)
):
    updated_user = await user_service.update_user(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
