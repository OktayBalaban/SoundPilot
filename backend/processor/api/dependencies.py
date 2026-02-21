from services.remote_storage import RemoteStorageService
from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner
from api.config import settings

def get_storage_service():
    return RemoteStorageService(endpoint="http://localhost:8001")

def get_processor_service():
    runner = DemucsRunner(model_name=settings.demucs_model)
    storage = get_storage_service()
    return ProcessorService(runner, storage)