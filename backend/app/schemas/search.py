from pydantic import BaseModel
from typing import Optional
from app.core.constants import SIMILARITY_THRESHOLD

class SearchRequest(BaseModel):
    query: str
    threshold: float = SIMILARITY_THRESHOLD

class SearchResponse(BaseModel):
    found: bool
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    similarity: Optional[float] = None