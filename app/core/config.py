from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql://user:pass@localhost/silph_users"

    JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()

