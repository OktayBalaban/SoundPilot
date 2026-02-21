from pydantic import BaseModel

class UploadResponse(BaseModel):
    url: str

class DeleteResponse(BaseModel):
    status: str