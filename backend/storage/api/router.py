import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from api.models import UploadResponse, DeleteResponse
from services.local_storage import LocalStorageService

router = APIRouter()

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
storage_service = LocalStorageService(
    base_path=STORAGE_DIR, 
    static_url_prefix="http://localhost:8001/files"
)

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