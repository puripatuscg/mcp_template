from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IMAGE_API_BASE_URL: str = "http://localhost:8080"
    IMAGE_API_KEY: str = ""
    TRANSPORT: Literal["stdio", "http"] = "stdio"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
