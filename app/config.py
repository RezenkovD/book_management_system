from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    SQLALCHEMY_DATABASE_URI: str


settings = Settings()
