import os

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api"
    API_V1_STR: str = "/v1"
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> str | list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    TESTING : bool = os.getenv("TESTING")

    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TEST_DATABASE_URI: str = os.getenv("TEST_DATABASE_URL")

    EMAIL_TEST_USER: EmailStr = "test@mail.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    FIRST_SUPERUSER_NAME: str = os.getenv("FIRST_SUPERUSER_NAME")

    USERS_OPEN_REGISTRATION: bool

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
