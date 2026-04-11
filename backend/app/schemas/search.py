from pydantic import BaseModel, field_validator
from typing import Optional
from app.core.constants import SIMILARITY_THRESHOLD

class SearchRequest(BaseModel):
    query: str

    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Query must be at least 2 characters")
        if len(v) > 500:
            raise ValueError("Query must be under 500 characters")
        return v

class SearchResponse(BaseModel):
    found: bool
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    similarity: Optional[float] = None