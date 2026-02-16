from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from .models import ProcessResponse, StemSelection
from .dependencies import get_processor_service
from services.processor_service import ProcessorService

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_audio(
    file: UploadFile = File(...),
    selection: StemSelection = Depends(),
    service: ProcessorService = Depends(get_processor_service)
):
    try:
        contents = await file.read()
        
        selection_dict = selection.model_dump() if hasattr(selection, 'model_dump') else selection.dict()
        stems_to_process = [k for k, v in selection_dict.items() if v]
        
        processed_bytes = service.process_audio_file(contents, stems_to_process)
        
        saved_result = service.save_results(processed_bytes)

        return ProcessResponse(
            job_id=saved_result["job_id"],
            status="completed",
            processed_files=saved_result["paths"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))