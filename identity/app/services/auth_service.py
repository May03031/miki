from datetime import datetime, timedelta, timezone
from typing import Optional
import uuid

from fastapi import HTTPException, status, Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import User, UserAuth, UserBalance, RefreshToken, LoginHistory, AuthProvider
from app.schemas.auth import RegisterSchema, LoginSchema, OAuthLoginSchema
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, 
    get_token_hash, verify_token_hash
)
from config import settings
import logging

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _log_login(self, user_id: uuid.UUID, app_code: str, method: str, request: Request):
        """Helper to log login history"""
        logging.basicConfig(level=logging.INFO)
        logging.info("User logged in")
        
        history = LoginHistory(
            user_id=user_id,
            app_code=app_code,
            login_method=method,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        self.db.add(history)
        # No commit here, we rely on the main transaction

    async def _get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.auth)).where(User.email == email)
        )
        return result.scalars().first()

    async def register_email(self, data: RegisterSchema, request: Request):
        existing_user = await self._get_user_by_email(data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # 1. Create User
        new_user = User(email=data.email)
        self.db.add(new_user)
        await self.db.flush() # Get ID

        # 2. Create Auth Record
        user_auth = UserAuth(
            user_id=new_user.id,
            provider=AuthProvider.EMAIL,
            password_hash=get_password_hash(data.password)
        )
        self.db.add(user_auth)

        # 3. Create Balance
        balance = UserBalance(user_id=new_user.id)
        self.db.add(balance)

        # 4. Log "Login" (Registration counts as first login usually, or we skip)
        await self._log_login(new_user.id, data.app_code, "email_register", request)
        
        await self.db.commit()
        
        return await self.create_tokens(new_user, data.app_code)

    async def login_email(self, data: LoginSchema, request: Request):
        user = await self._get_user_by_email(data.email)
        if not user:
            # Prevent enumeration by using same error
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Enforce Method
        if user.auth.provider != AuthProvider.EMAIL:
            raise HTTPException(status_code=400, detail=f"Please login with {user.auth.provider.value}")

        if not verify_password(data.password, user.auth.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        await self._log_login(user.id, data.app_code, "email", request)
        await self.db.commit()

        return await self.create_tokens(user, data.app_code)

    async def verify_google_token(self, id_token: str) -> str:
        # MOCK: In production use google.oauth2.id_token.verify_oauth2_token
        if "invalid" in id_token:
            raise HTTPException(status_code=401, detail="Invalid Google Token")
        return "mock_user@gmail.com"

    async def login_google(self, data: OAuthLoginSchema, request: Request):
        email = await self.verify_google_token(data.id_token)
        
        user = await self._get_user_by_email(email)
        
        if user:
            # Enforce "One Method"
            if user.auth.provider != AuthProvider.GOOGLE:
                 raise HTTPException(status_code=400, detail=f"Account exists. Please login with {user.auth.provider.value}")
        else:
            # Auto-Register
            user = User(email=email)
            self.db.add(user)
            await self.db.flush()
            
            user_auth = UserAuth(user_id=user.id, provider=AuthProvider.GOOGLE)
            self.db.add(user_auth)
            
            balance = UserBalance(user_id=user.id)
            self.db.add(balance)

        await self._log_login(user.id, data.app_code, "google", request)
        await self.db.commit()
        
        return await self.create_tokens(user, data.app_code)

    async def verify_apple_token(self, id_token: str) -> str:
        # MOCK: Verify Apple Identity Token logic
        # Production: Decode JWT header, fetch Apple public keys, verify signature & audience
        if "invalid" in id_token:
            raise HTTPException(status_code=401, detail="Invalid Apple Token")
        # In real flow, extract email from the decoded token claims
        return "mock_apple_user@icloud.com"

    async def login_apple(self, data: OAuthLoginSchema, request: Request):
        email = await self.verify_apple_token(data.id_token)
        
        user = await self._get_user_by_email(email)
        
        if user:
            # Enforce "One Method"
            if user.auth.provider != AuthProvider.APPLE:
                 raise HTTPException(status_code=400, detail=f"Account exists. Please login with {user.auth.provider.value}")
        else:
            # Auto-Register for Apple
            user = User(email=email)
            self.db.add(user)
            await self.db.flush()
            
            user_auth = UserAuth(user_id=user.id, provider=AuthProvider.APPLE)
            self.db.add(user_auth)
            
            balance = UserBalance(user_id=user.id)
            self.db.add(balance)

        await self._log_login(user.id, data.app_code, "apple", request)
        await self.db.commit()
        
        return await self.create_tokens(user, data.app_code)

    async def get_user_profile(self, user_id: uuid.UUID):
        result = await self.db.execute(
            select(User)
            .options(
                selectinload(User.auth),
                selectinload(User.balance)
            )
            .where(User.id == user_id)
        )

        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": str(user.id),
            "email": user.email,
            "provider": user.auth.provider if user.auth else None,
            "balance": user.balance.amount if user.balance else 0,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }


    
    async def create_tokens(self, user: User, app_code: str):
        access_token = create_access_token(user.id, app_code)
        
        random_part = create_refresh_token()
        # Prefix with u{uuid}. to allow fast DB lookup on rotation
        final_refresh_token = f"u{user.id}.{random_part}"
        
        hashed_secret = get_token_hash(random_part)
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        db_token = RefreshToken(
            user_id=user.id,
            token_hash=hashed_secret,
            expires_at=expires_at
        )
        self.db.add(db_token)
        await self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": final_refresh_token,
            "token_type": "bearer"
        }

    async def rotate_refresh_token(self, raw_refresh_token: str, app_code: str):
        try:
            user_part, secret_part = raw_refresh_token.split('.', 1)
            uid_str = user_part[1:] # remove 'u'
            user_uuid = uuid.UUID(uid_str)
        except:
             raise HTTPException(status_code=401, detail="Invalid token format")

        result = await self.db.execute(
            select(RefreshToken)
            .where(RefreshToken.user_id == user_uuid)
            .where(RefreshToken.revoked == False)
        )
        active_tokens = result.scalars().all()
        
        target_token_row = None
        for t in active_tokens:
            if verify_token_hash(secret_part, t.token_hash):
                target_token_row = t
                break
        
        if not target_token_row:
            raise HTTPException(status_code=401, detail="Invalid or revoked token")

        if target_token_row.expires_at < datetime.now(timezone.utc):
            target_token_row.revoked = True
            await self.db.commit()
            raise HTTPException(status_code=401, detail="Token expired")

        target_token_row.revoked = True
        
        user = await self.db.get(User, user_uuid)
        return await self.create_tokens(user, app_code)