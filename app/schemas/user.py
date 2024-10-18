from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserLoginRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
        from_attributes = True
