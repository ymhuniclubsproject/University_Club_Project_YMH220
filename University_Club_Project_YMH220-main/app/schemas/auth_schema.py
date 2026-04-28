from pydantic import BaseModel
from typing import Optional

class Token(BaseModel): # Schema for returning the JWT access token and its type | JWT erişim jetonunu ve türünü döndürmek için kullanılan şema
    access_token: str
    token_type: str

class TokenData(BaseModel): # Represents the payload data extracted from a decoded token | Kodu çözülmüş bir jetondan çıkarılan yük verilerini temsil eder
    email: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel): # Schema for validating user credentials during the login process | Giriş işlemi sırasında kullanıcı bilgilerini doğrulamak için kullanılan şema
    email: str
    password: str