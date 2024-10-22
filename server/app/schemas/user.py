from typing import List

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class SubscriptionSummary(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    subscriptions: List[SubscriptionSummary] = []
    subscribers: List[SubscriptionSummary] = []

    class Config:
        orm_mode = True
        from_attributes = True
