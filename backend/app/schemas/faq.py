from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.schemas.base import SchemaBase

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Question must be at least 5 characters")
        if len(v) > 500:
            raise ValueError("Question must be under 500 characters")
        return v

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Answer must be at least 5 characters")
        if len(v) > 2000:
            raise ValueError("Answer must be under 2000 characters")
        return v

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

    @field_validator("question")
    @classmethod
    def validate_question(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if len(v) < 5:
                raise ValueError("Question must be at least 5 characters")
            if len(v) > 500:
                raise ValueError("Question must be under 500 characters")
        return v

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if len(v) < 5:
                raise ValueError("Answer must be at least 5 characters")
            if len(v) > 2000:
                raise ValueError("Answer must be under 2000 characters")
        return v

class FAQResponse(SchemaBase):
    id: int
    question: str
    answer: str
    category: Optional[str]
    created_at: datetime