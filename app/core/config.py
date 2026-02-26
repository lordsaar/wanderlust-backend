from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    anthropic_api_key: str = ""
    database_url: str = "postgresql://wanderlust:wanderlust@db:5432/wanderlust"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()