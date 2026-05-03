from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SoundPilot Processor"
    debug: bool = False
    demucs_model: str = "htdemucs"
    STORAGE_API_BASE_URL: str = "http://localhost:8001"


settings = Settings()