from pydantic import BaseModel
from datetime import datetime
from app.schemas.base import SchemaBase

class UnansweredResponse(SchemaBase):
    id: int
    question: str
    frequency: int
    created_at: datetime
    last_asked_at: datetime

class ConvertToFAQRequest(BaseModel):
    answer: str
    category: str = "General"