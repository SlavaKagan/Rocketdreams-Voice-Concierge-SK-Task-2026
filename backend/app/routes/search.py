import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.constants import SIMILARITY_THRESHOLD
from app.schemas.search import SearchRequest, SearchResponse
from app.services.embedding import get_embedding
from app.repositories import faq as faq_repo
from app.repositories import unanswered as unanswered_repo

router = APIRouter(prefix="/api", tags=["Search"])
logger = logging.getLogger("meridian.routes.search")

@router.post("/search", response_model=SearchResponse)
def search_faq(request: SearchRequest, db: Session = Depends(get_db)):
    logger.info(f"Search query: '{request.query}'")
    embedding = get_embedding(request.query)
    result = faq_repo.search_by_embedding(db, embedding)

    if result:
        row, similarity = result
        if similarity >= SIMILARITY_THRESHOLD:
            logger.info(f"Match found: similarity={similarity:.3f} faq='{row.question}'")
            return SearchResponse(
                found=True,
                question=row.question,
                answer=row.answer,
                category=row.category,
                similarity=similarity
            )

    logger.info(f"No match found for query: '{request.query}'")
    unanswered_repo.record(db, request.query)
    return SearchResponse(found=False)