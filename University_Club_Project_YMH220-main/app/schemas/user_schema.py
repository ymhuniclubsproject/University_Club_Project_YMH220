from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import RoleEnum

class UserBase(BaseModel): # Shared attributes representing core user information | Temel kullanıcı bilgilerini temsil eden ortak özellikler
    full_name: str
    email: EmailStr

class UserCreate(UserBase): # Schema for validating data during user registration | Kullanıcı kaydı sırasında verileri doğrulamak için kullanılan şema
    password: str
    role: Optional[RoleEnum] = RoleEnum.student

class UserUpdate(BaseModel): # Schema for partial updates to an existing user's profile | Mevcut bir kullanıcı profilinin kısmi güncellenmesi için kullanılan şema
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role: Optional[RoleEnum] = None

class UserResponse(UserBase): # Schema for returning user data with metadata and database-generated fields | Üst veriler ve veri tabanı alanlarıyla birlikte kullanıcı verilerini döndürmek için şema
    id: int
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True} # Compatibility with ORM models | ORM modelleri ile uyumluluğu sağlar