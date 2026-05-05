from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User, RoleEnum
from app.core.security import verify_password, create_access_token, settings
from app.repositories.user_repository import UserRepository
from jose import JWTError, jwt
from app.schemas.auth_schema import TokenData
from pydantic import ValidationError

# Configures the OAuth2 scheme with specific permission scopes | Belirli yetki kapsamları ile OAuth2 şemasını yapılandırır
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={
        "student": "Student privileges",
        "club_manager": "Club manager privileges",
        "admin": "Admin privileges"
    }
)

class AuthService: # Orchestrates user authentication and credential verification | Kullanıcı kimlik doğrulama ve bilgi doğrulama işlemlerini yönetir
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate_user(self, email: str, password: str) -> User | None: # Validates email and password against the database | E-posta ve şifreyi veri tabanına göre doğrular
        user = self.repo.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User: # Decodes JWT and validates user roles and permissions | JWT kodunu çözer, kullanıcı rollerini ve yetkilerini doğrular
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    try:
        # Decodes the JWT token using the secret key | Gizli anahtarı kullanarak JWT jetonunun kodunu çözer
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise credentials_exception
        
    repo = UserRepository(db)
    user = repo.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
        
    # Verifies if the user's role matches the required security scopes | Kullanıcı rolünün gerekli güvenlik kapsamlarıyla eşleşip eşleşmediğini doğrular
    if security_scopes.scopes and token_data.role not in security_scopes.scopes:
        # Grants access if the user is an admin, even if the specific scope is missing | Özel kapsam eksik olsa bile kullanıcı admin ise erişim izni verir
        if token_data.role != RoleEnum.admin.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User: # Ensures the authenticated user's account is currently active | Kimliği doğrulanmış kullanıcı hesabının aktif olduğundan emin olur
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user