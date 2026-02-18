from services.local_storage import LocalStorageService
from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner
from api.config import settings
import os

def get_storage_service():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "outputs")
    
    return LocalStorageService(
        base_path=output_path,
        static_url_prefix="/static"
    )

def get_processor_service():
    runner = DemucsRunner(model_name=settings.demucs_model)
    storage = get_storage_service()
    return ProcessorService(runner, storage)