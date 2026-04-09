from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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