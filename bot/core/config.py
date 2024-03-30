from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    database_url: str = 'sqlite+aiosqlite:///./avapro.db'
    model_config = SettingsConfigDict(
        env_file='../.env', env_file_encoding='utf-8'
    )


settings = Settings()
