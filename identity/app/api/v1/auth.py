from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.schemas.auth import (
    RegisterSchema, LoginSchema, OAuthLoginSchema, 
    TokenSchema, RefreshTokenSchema, UserProfileSchema
)
from app.services.auth_service import AuthService
from app.db.deps import get_db
from config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


# OAuth2 Scheme để Swagger UI hiển thị nút Authorize
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/email")

# Dependency để giải mã token và lấy user_id
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

router = APIRouter()

@router.post("/register/email", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def register_email(
    data: RegisterSchema, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.register_email(data, request)

@router.post("/login/email", response_model=TokenSchema)
async def login_email(
    data: LoginSchema, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.login_email(data, request)

@router.post("/login/google", response_model=TokenSchema)
async def login_google(
    data: OAuthLoginSchema, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.login_google(data, request)

@router.post("/login/apple", response_model=TokenSchema)
async def login_apple(
    data: OAuthLoginSchema, 
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Apple Login: Requires ID Token from Apple Sign-In on client side.
    """
    service = AuthService(db)
    return await service.login_apple(data, request)

@router.get("/me", response_model=UserProfileSchema)
async def get_current_user_profile(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Protected Endpoint: Returns user profile, balance, and auth provider.
    """
    service = AuthService(db)
    return await service.get_user_profile(uuid.UUID(user_id))

@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    data: RefreshTokenSchema,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.rotate_refresh_token(data.refresh_token, data.app_code)