from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    database_url: str = "postgresql://wanderlust:wanderlust@db:5432/wanderlust"

    class Config:
        env_file = ".env"

settings = Settings()
