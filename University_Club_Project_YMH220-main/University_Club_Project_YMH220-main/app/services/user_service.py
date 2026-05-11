from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import get_password_hash
from app.models.user import User

class UserService: # Business logic layer for managing user operations | Kullanıcı işlemlerini yöneten iş mantığı katmanı
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> User: # Orchestrates the registration process including validation and hashing | Doğrulama ve hashleme dahil kayıt sürecini yönetir
        # Prevents duplicate registrations using the same email | Aynı e-posta ile mükerrer kayıtları önler
        if self.repo.get_user_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Secures the password before database storage | Veri tabanı kaydından önce şifreyi güvenli hale getirir
        hashed_password = get_password_hash(user_in.password)
        new_user = self.repo.create_user(user_in, hashed_password)
        return new_user

    def get_user(self, user_id: int) -> User: # Retrieves a user and handles the error if not found | Kullanıcıyı getirir ve bulunamazsa hata yönetimini yapar
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user