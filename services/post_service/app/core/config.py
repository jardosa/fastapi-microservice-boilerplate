from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./post_service.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

