""" App Environment Configuration """
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Required environment variables"""

    POSTGRES_SERVER: str = Field("sql_db")
    POSTGRES_USER: str = Field("postgres")
    POSTGRES_PASSWORD: str = Field("postgres")
    POSTGRES_DB: str = Field("app")
    SECRET_KEY: str = Field(
        "44e6ea2c51a9775277fb17cadf2dd616671faf96a1deeb214aa48fe2ffa37500"
    )
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30)


settings = Settings()
