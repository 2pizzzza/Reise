from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.subscription import SubscriptionRepository


class SubscriptionService:
    def __init__(self, db: Session):
        self.subscription_repository = SubscriptionRepository(db)

    def subscribe(self, user_id: int, target_user_id: int):
        if self.subscription_repository.is_subscribed(user_id, target_user_id):
            raise HTTPException(status_code=400, detail="Already subscribed")
        return self.subscription_repository.subscribe(user_id, target_user_id)

    def unsubscribe(self, user_id: int, target_user_id: int):
        if not self.subscription_repository.is_subscribed(user_id, target_user_id):
            raise HTTPException(status_code=400, detail="Not subscribed")
        self.subscription_repository.unsubscribe(user_id, target_user_id)
