from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    app_code: str = Field(..., description="Identifier of the calling application")

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    app_code: str

class OAuthLoginSchema(BaseModel):
    id_token: str = Field(..., description="JWT received from Google/Apple client SDK")
    app_code: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str
    app_code: str

class UserProfileSchema(BaseModel):
    id: UUID
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    provider: str
    balance: float
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    
    class Config:
        from_attributes = True