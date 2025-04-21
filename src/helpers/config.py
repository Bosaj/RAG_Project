from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_EXTENSIONS: list[str] = ["txt", "csv", "xls", "xlsx", "json"]
    FILE_ALLOWED_TYPES: list[str] = ["text/plain", "text/csv", "application/vnd.ms-excel", "application/json"]
    FILE_MAX_SIZE: int = 10  # in MB
    FILE_DEFAULT_CHUNK_SIZE: int = 1024 * 1024  # 1 MB

    MONGODB_URL:str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
    