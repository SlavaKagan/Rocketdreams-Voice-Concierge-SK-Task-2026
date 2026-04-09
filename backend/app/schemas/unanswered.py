from pydantic import BaseModel
from datetime import datetime

class UnansweredResponse(BaseModel):
    id: int
    question: str
    frequency: int
    created_at: datetime
    last_asked_at: datetime

    class Config:
        from_attributes = True

class ConvertToFAQRequest(BaseModel):
    answer: str
    category: str = "General"