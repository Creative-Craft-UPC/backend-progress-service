from datetime import datetime
from pydantic import BaseModel, Field
import pytz

lima_tz = pytz.timezone("America/Lima")

class AttemptSchema(BaseModel):
    time: float
    errors_quantity: int
    date: str = Field(default_factory=lambda: datetime.now(lima_tz).replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S"))

class AttemptDto(BaseModel):
    time: float
    errors_quantity: int


class AttemptResponse(AttemptSchema):
    id: str = Field(..., example="665f1b0c543ed91f9a1d0ef9")
    