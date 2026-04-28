from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user_schema import UserResponse
from app.services.auth_service import get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse) # Endpoint to retrieve the profile of the authenticated user | Kimliği doğrulanmış kullanıcının profilini getirmek için uç nokta
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get the currently logged in user based on their JWT token.
    """
    return current_user # Returns user data extracted from the verified access token | Doğrulanmış erişim jetonundan çıkarılan kullanıcı verilerini döndürür