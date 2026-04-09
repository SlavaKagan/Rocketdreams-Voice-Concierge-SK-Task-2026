from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.base import SchemaBase

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

class FAQResponse(SchemaBase):
    id: int
    question: str
    answer: str
    category: Optional[str]
    created_at: datetime