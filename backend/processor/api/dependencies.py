from services.local_storage import LocalStorageService
from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner
from api.config import settings
import os

def get_storage_service():
    # Artık LocalStorageService yerine RemoteStorageService dönüyoruz
    return RemoteStorageService(base_url="http://localhost:8001")

def get_processor_service():
    runner = DemucsRunner(model_name=settings.demucs_model)
    storage = get_storage_service()
    return ProcessorService(runner, storage)