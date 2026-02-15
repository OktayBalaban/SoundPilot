from pydantic import BaseModel


class StemSelection(BaseModel):
    vocals: bool = True
    drums: bool = True
    bass: bool = True
    other: bool = True
