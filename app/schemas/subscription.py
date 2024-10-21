from pydantic import BaseModel


class SubscriptionRequest(BaseModel):
    target_user_id: int


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    target_user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
