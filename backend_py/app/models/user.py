# app/models/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr
    avatar: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., example="strongpassword")

class UserResponse(UserBase):
    id: str
