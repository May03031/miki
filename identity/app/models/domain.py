import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from app.db.base import Base

from sqlalchemy import (
    String, Boolean, DateTime, ForeignKey, 
    DECIMAL, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    APPLE = "apple"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    auth: Mapped["UserAuth"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    balance: Mapped["UserBalance"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class UserAuth(Base):
    __tablename__ = "user_auth"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    provider: Mapped[AuthProvider] = mapped_column(String(50), nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Only for Email provider
    
    user: Mapped["User"] = relationship(back_populates="auth")

class UserBalance(Base):
    __tablename__ = "user_balances"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(18, 4), default=0)
    currency: Mapped[str] = mapped_column(String(3), default="USD")

    user: Mapped["User"] = relationship(back_populates="balance")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String, index=True) # Hashed version of the token
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata for rotation tracking (optional, but good for security auditing)
    replaced_by: Mapped[Optional[str]] = mapped_column(String, nullable=True) 

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

class LoginHistory(Base):
    __tablename__ = "user_login_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    app_code: Mapped[str] = mapped_column(String(50), nullable=False)
    login_method: Mapped[str] = mapped_column(String(50))
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())