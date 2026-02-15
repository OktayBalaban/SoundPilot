import io
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from .models import StemSelection
from .dependencies import get_processor_service
from services.processor_service import ProcessorService

router = APIRouter()

# api/router.py
@router.post("/process")
async def process_audio(
    file: UploadFile = File(...),
    selection: StemSelection = StemSelection(),
    service: ProcessorService = Depends(get_processor_service)
):
    contents = await file.read()
    
    settings = selection.model_dump() if hasattr(selection, 'model_dump') else selection.dict()
    
    processed_bytes = service.process_audio_file(contents, settings)
    
    return StreamingResponse(
        io.BytesIO(processed_bytes), 
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename=processed_{file.filename}"}
    )