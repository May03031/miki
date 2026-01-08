from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
import hashlib
import hmac
import secrets

from config import settings


# =====================================================
# Crypt Context (chỉ dùng cho PASSWORD)
# =====================================================
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# =====================================================
# Helpers
# =====================================================
def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# =====================================================
# Password Hashing (FIX 72 BYTES)
# =====================================================
def get_password_hash(password: str) -> str:
    """
    Password hashing chuẩn:
    SHA-256 -> bcrypt
    - Không giới hạn độ dài
    - An toàn với Unicode / emoji
    """
    return pwd_context.hash(_sha256(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_sha256(plain_password), hashed_password)


# =====================================================
# Refresh Token Hashing 
# =====================================================
def get_token_hash(token: str) -> str:
    """
    Hash refresh token để lưu DB.
    Dùng HMAC-SHA256 để:
    - Không lỗi 72 bytes
    - Nhanh
    - Token leak DB vẫn không dùng được
    """
    return hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def verify_token_hash(token: str, hashed_token: str) -> bool:
    expected = get_token_hash(token)
    return hmac.compare_digest(expected, hashed_token)


# =====================================================
# JWT Handling 
# =====================================================
def create_access_token(subject: Union[str, Any], app_code: str) -> str:
    """
    JWT Access Token (stateless)
    - Không hash
    - Không lưu DB
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "sub": str(subject),
        "app_code": app_code,
        "exp": expire,
        "type": "access"
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# =====================================================
# Refresh Token Generator (Opaque Token)
# =====================================================
def create_refresh_token() -> str:
    """
    Sinh refresh token:
    - KHÔNG phải JWT
    - High entropy
    - Chỉ lưu bản HASH trong DB
    """
    return secrets.token_urlsafe(64)
