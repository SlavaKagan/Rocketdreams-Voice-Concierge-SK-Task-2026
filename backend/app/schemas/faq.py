from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = "General"

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

class FAQResponse(BaseModel):
    id: int
    question: str
    answer: str
    category: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True