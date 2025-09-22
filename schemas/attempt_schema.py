from datetime import datetime
from pydantic import BaseModel, Field

class AttemptSchema(BaseModel):
    time: float
    errors_quantity: int
    date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class AttemptDto(BaseModel):
    time: float
    errors_quantity: int


class AttemptResponse(AttemptSchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    