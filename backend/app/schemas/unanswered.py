from pydantic import BaseModel, field_validator
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

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Answer must be at least 5 characters")
        if len(v) > 2000:
            raise ValueError("Answer must be under 2000 characters")
        return v