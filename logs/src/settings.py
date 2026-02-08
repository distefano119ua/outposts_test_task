from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    NGINX_LOGS_URL: str = Field(..., env="NGINX_LOGS_URL")
    EXPORT_LOGS_DIR: str = Field(..., env="EXPORT_LOGS_DIR")
    GITHUB_TOKEN: str = Field(..., description="GitHub personal access token")
    GITHUB_REPO: str = Field(..., description="owner/repo")
    GITHUB_BRANCH: str = Field(default="main")
    GITHUB_EXPORTS_PATH: str = Field(default="exports")

    class Config:
        env_file = ".env"
        env_prefix = ""

settings = Settings()
