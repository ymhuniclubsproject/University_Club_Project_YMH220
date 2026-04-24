from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import RoleEnum

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[RoleEnum] = RoleEnum.student

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[RoleEnum] = None

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
