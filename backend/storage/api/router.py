import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.models import UploadResponse, DeleteResponse, LibraryResponse, MetadataRequest
from services.local_storage import LocalStorageService
from services.local_library import LocalLibraryService
from core.stem_validator import StemValidator
from core.metadata_service import MetadataService

router = APIRouter()

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STATIC_PREFIX = "http://localhost:8001/files"

storage_service = LocalStorageService(
    base_path=STORAGE_DIR,
    static_url_prefix=STATIC_PREFIX
)

library_service = LocalLibraryService(
    base_path=STORAGE_DIR,
    static_url_prefix=STATIC_PREFIX,
    validator=StemValidator(),
    metadata=MetadataService()
)

metadata_service = MetadataService()

@router.post("/upload/{job_id}", response_model=UploadResponse)
async def upload_file(job_id: str, stem_name: str, file: UploadFile = File(...)):
    try:
        content = await file.read()
        url = storage_service.save_result(job_id, stem_name, content)
        return UploadResponse(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/jobs/{job_id}", response_model=DeleteResponse)
async def delete_job(job_id: str):
    try:
        storage_service.delete_job(job_id)
        return DeleteResponse(status="deleted")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/library", response_model=LibraryResponse)
async def list_library():
    songs = library_service.list_songs()
    return LibraryResponse(songs=songs, total=len(songs))


@router.get("/library/{song_id}")
async def get_song(song_id: str):
    song = library_service.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.delete("/library/{song_id}", response_model=DeleteResponse)
async def delete_song(song_id: str):
    deleted = library_service.delete_song(song_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Song not found")
    return DeleteResponse(status="deleted")


@router.post("/library/{song_id}/metadata")
async def save_metadata(song_id: str, request: MetadataRequest):
    song_dir = os.path.join(STORAGE_DIR, song_id)
    if not os.path.isdir(song_dir):
        raise HTTPException(status_code=404, detail="Song not found")
    meta = metadata_service.write(song_dir, request.title, request.source_url)
    return meta