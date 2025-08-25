# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole

class UserCreate(BaseModel):
    phone: str
    email: Optional[EmailStr]
    fullname: Optional[str]
    role: Optional[UserRole] = UserRole.xaridor
    password: str

class UserRead(BaseModel):
    id: int
    phone: str
    email: Optional[EmailStr]
    fullname: Optional[str]
    role: UserRole

    class Config:
        orm_mode = True
