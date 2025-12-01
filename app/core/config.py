from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    BASE_URL: str = os.getenv("BASE_URL", "")

    FERNET_KEY: str = os.getenv("FERNET_KEY", "")

settings = Settings()