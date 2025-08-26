
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URL: str
    SMS_API_URL: str
    SMS_API_KEY: str
    SMS_SENDER: str

    class Config:
        env_file = ".env"  

settings = Settings()
