from dotenv import load_dotenv
import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    bot_token: SecretStr = os.getenv("BOT_TOKEN")
    database_url: str = os.getenv("DATABASE_URL")
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


settings = Settings()
