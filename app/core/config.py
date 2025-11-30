from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    # BASE_URL: str = os.getenv("BASE_URL", "http://srv01.dev.keycenter.ai:8046")
    BASE_URL: str = os.getenv("BASE_URL", "https://965d81d8f9f8.ngrok-free.app")

    FERNET_KEY: str = os.getenv("FERNET_KEY", "")
    BEARER_FERNET_KEY: str = os.getenv("BEARER_FERNET_KEY", "")
    STATIC_BEARER_TOKEN: str = os.getenv("STATIC_BEARER_TOKEN", "")
    x_session_token : str = os.getenv("X_SESSION_TOKEN","")

settings = Settings()