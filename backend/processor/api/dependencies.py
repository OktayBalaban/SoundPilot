from services.remote_storage import RemoteStorageService
from services.processor_service import ProcessorService
from services.demucs_runner import DemucsRunner
from services.youtube_downloader import YouTubeDownloader
from api.config import settings


def get_storage_service():
    return RemoteStorageService(endpoint=settings.STORAGE_API_BASE_URL)


def get_processor_service():
    runner = DemucsRunner(model_name=settings.demucs_model)
    storage = get_storage_service()
    downloader = YouTubeDownloader()
    return ProcessorService(runner, storage, downloader)