from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from .models import ProcessResponse, StemSelection, URLRequest
from .dependencies import get_processor_service
from services.processor_service import ProcessorService

router = APIRouter()

ALL_STEMS = ["vocals", "drums", "bass", "other"]


@router.post("/process", response_model=ProcessResponse)
async def process_audio(
    file: UploadFile = File(...),
    selection: StemSelection = Depends(),
    service: ProcessorService = Depends(get_processor_service)
):
    try:
        contents = await file.read()
        stems = [k for k, v in selection.model_dump().items() if v] or ALL_STEMS

        title = file.filename.rsplit('.', 1)[0] if file.filename else None

        processed_data = service.process_audio_file(contents, stems)
        saved_result = service.save_results(processed_data, title=title)
        service.storage.save_metadata(saved_result["job_id"], title or saved_result["job_id"])

        return ProcessResponse(
            job_id=saved_result["job_id"],
            status="completed",
            processed_files=saved_result["paths"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process-url", response_model=ProcessResponse)
async def process_url(
    request: URLRequest,
    service: ProcessorService = Depends(get_processor_service)
):
    try:
        result = service.process_url(request.url, ALL_STEMS)

        return ProcessResponse(
            job_id=result["job_id"],
            status="completed",
            processed_files=result["paths"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))