from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Sound Processor"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Demucs Specific
    demucs_model: str = "htdemucs"
    demucs_stems: str = "vocals"

    # Automatically load from .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()