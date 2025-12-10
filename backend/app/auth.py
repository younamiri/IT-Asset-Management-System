from datetime import datetime, timedelta
from typing import Optional
import jwt
from . config import settings

def create_access_token(data:  dict, expires_delta: Optional[timedelta] = None):
    """
    ایجاد JWT Token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    تائید JWT Token
    """
    try:
        payload = jwt. decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None

# Active Directory Authentication (در مراحل بعدی پکامل می‌شود)
def authenticate_user_ad(username: str, password: str):
    """
    احراز هویت کاربر از طریق Active Directory
    """
    # این تابع در مرحله بعدی پکامل می‌شود
    pass
