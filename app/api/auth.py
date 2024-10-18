from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, User
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)
    return AuthService(user_service)


@router.post("/signup", response_model=User)
async def signup(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.create_user(user)


@router.post("/signin")
async def signin(form_data: OAuth2PasswordRequestForm = Depends(),
                 auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
