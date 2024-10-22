from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserLoginRequest
from app.services.auth import AuthService
from app.db.database import get_db
from app.core.security import get_current_user
from app.schemas.subscription import SubscriptionResponse, SubscriptionRequest
from app.services.subscription import SubscriptionService

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup(user_create: UserCreate, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.create_user(user_create)
    return UserResponse.from_orm(user)


@router.post("/signin")
def signin(req: UserLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.user_repository.get_user_by_email(req.email)
    if not user or not auth_service.verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserResponse)
def get_profile(
        username: str = None,
        db: Session = Depends(get_db),
        current_user: UserResponse = Depends(get_current_user)
):
    service = AuthService(db)
    if username:
        return service.get_profile(user_name=username)
    else:
        return service.get_profile(user_id=current_user.id)


@router.put("/updateProfile", response_model=UserResponse)
def update_profile(
        user_update: UserCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/subscribe", response_model=SubscriptionResponse)
def subscribe(subscription_request: SubscriptionRequest, db: Session = Depends(get_db),
              current_user: UserResponse = Depends(get_current_user)):
    service = SubscriptionService(db)
    return service.subscribe(current_user.id, subscription_request.target_user_id)


@router.post("/unsubscribe", status_code=204)
def unsubscribe(subscription_request: SubscriptionRequest, db: Session = Depends(get_db),
                current_user: UserResponse = Depends(get_current_user)):
    service = SubscriptionService(db)
    service.unsubscribe(current_user.id, subscription_request.target_user_id)
