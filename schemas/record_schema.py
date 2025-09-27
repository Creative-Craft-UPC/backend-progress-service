from pydantic import BaseModel, Field
from typing import Optional, List

from schemas.attempt_schema import AttemptResponse

class RecordSchema(BaseModel):
    max_time: float
    min_time: float
    attempts: Optional[List[str]] = Field(default_factory=list, example=["665f1b0c543ed91f9a1d0ef9","665f1b0c543ed91f9a1d0ef9"])
    total_errors: int
    exercice_id: Optional[str] = Field(..., example="665f1b0c543ed91f9a1d0ef9")

class RecordResponse(BaseModel):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    max_time: float
    min_time: float
    attempts: List[AttemptResponse]
    total_errors: int
    exercice_id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    