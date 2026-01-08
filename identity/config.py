from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field
from typing import ClassVar

class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Microservice"
    API_V1_STR: str = "/api/v1"

    AUTO_CREATE_TABLES: int = 1

    # Database
    POSTGRES_USER: str = "ai_user"
    POSTGRES_PASSWORD: str = "123456"
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "kimi_system"

   
    # PostgreSQL connection
    #DATABASE_URL: str = "postgresql+psycopg://ai_user:123456@db:5432/kimi_system"



    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",  #asyncpg
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))

    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_TO_A_LONG_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # OAuth Clients (Placeholders)
    GOOGLE_CLIENT_ID: str = "72486842231-3seh2sipn1at3309r449hc65rkjfglpk.apps.googleusercontent.com"
    APPLE_CLIENT_ID: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()