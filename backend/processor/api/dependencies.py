from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner

def get_processor_service() -> ProcessorService:
    runner = DemucsRunner() 
    return ProcessorService(runner)