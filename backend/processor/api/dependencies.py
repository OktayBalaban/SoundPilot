from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner

from api.config import settings

def get_processor_service() -> ProcessorService:
    runner = DemucsRunner(
        model_name=settings.demucs_model, 
        default_stems=settings.demucs_stems
    ) 
    return ProcessorService(runner)