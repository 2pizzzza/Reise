from sqlalchemy.orm import Session
from app.models.user import User, Subscription


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_name(self, username: str):
        return self.db.query(User).filter(User.name == username).first()

    def get_subscriptions(self, user_id: int):
        return self.db.query(User).join(Subscription, Subscription.target_user_id == User.id).filter(
            Subscription.user_id == user_id).all()

    def get_subscribers(self, user_id: int):
        return self.db.query(User).join(Subscription, Subscription.user_id == User.id).filter(
            Subscription.target_user_id == user_id).all()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
