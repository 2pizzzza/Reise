from sqlalchemy.orm import Session

from app.models.user import Subscription


class SubscriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def subscribe(self, user_id: int, target_user_id: int):
        subscription = Subscription(user_id=user_id, target_user_id=target_user_id)
        self.db.add(subscription)
        self.db.commit()
        self.db.refresh(subscription)
        return subscription

    def unsubscribe(self, user_id: int, target_user_id: int):
        subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user_id, Subscription.target_user_id == target_user_id
        ).first()
        if subscription:
            self.db.delete(subscription)
            self.db.commit()

    def is_subscribed(self, user_id: int, target_user_id: int) -> bool:
        return self.db.query(Subscription).filter(
            Subscription.user_id == user_id, Subscription.target_user_id == target_user_id
        ).count() > 0
