from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PATH_TO_FILE: str = Field(..., env="PATH_TO_FILE")

    class Config:
        env_file = "../.env"
        env_prefix = ""

settings = Settings()
