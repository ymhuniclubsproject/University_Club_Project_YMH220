from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import Token, LoginRequest
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.core.security import create_access_token, settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    """
    user_service = UserService(db)
    return user_service.register_user(user_in)

@router.post("/login", response_model=Token)
def login_for_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint to get a JWT access token.
    Accepts JSON body for frontend authentication.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(email=login_data.email, password=login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    role_str = user.role.value if hasattr(user.role, "value") else str(user.role)
    access_token = create_access_token(
        data={"email": user.email, "role": role_str},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
