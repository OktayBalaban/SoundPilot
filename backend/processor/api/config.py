from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Sound Processor"
    debug: bool = False
    
    # Demucs Ayarları
    demucs_model: str = "htdemucs"
    demucs_stems: str = "vocals"

    # --- ENJEKSİYON NOKTASI ---
    STORAGE_API_BASE_URL: str = "http://localhost:8001"

    # .env dosyasını da destekle (lokal geliştirme için)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()