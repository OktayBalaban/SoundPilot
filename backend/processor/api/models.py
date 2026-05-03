from pydantic import BaseModel
from typing import List

class StemSelection(BaseModel):
    vocals: bool = True
    drums: bool = True
    bass: bool = True
    other: bool = True

class ProcessResponse(BaseModel):
    job_id: str
    status: str
    processed_files: List[str]

class URLRequest(BaseModel):
    url: str