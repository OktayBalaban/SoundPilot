import io
from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from .models import StemSelection
from .dependencies import get_processor_service
from services.processor_service import ProcessorService

router = APIRouter()

@router.post("/process")
async def process_audio(
    file: UploadFile = File(...),
    selection: StemSelection = StemSelection(),
    service: ProcessorService = Depends(get_processor_service)
):
    contents = await file.read()
    
    selected_dict = selection.model_dump() if hasattr(selection, 'model_dump') else selection.dict()
    stems_to_process = [stem for stem, enabled in selected_dict.items() if enabled]
    
    processed_bytes_dict = service.process_audio_file(contents, stems_to_process)
    
    first_stem = list(processed_bytes_dict.values())[0]
    
    return StreamingResponse(
        io.BytesIO(first_stem), 
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename=processed_{file.filename}"}
    )