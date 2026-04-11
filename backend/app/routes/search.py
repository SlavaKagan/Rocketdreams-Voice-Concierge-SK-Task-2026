import logging
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.constants import SIMILARITY_THRESHOLD, RATE_LIMIT_SEARCH
from app.schemas.search import SearchRequest, SearchResponse
from app.services.embedding import get_embedding
from app.repositories import faq as faq_repo
from app.repositories import unanswered as unanswered_repo
from app.main import limiter

router = APIRouter(prefix="/api", tags=["Search"])
logger = logging.getLogger("meridian.routes.search")

@router.post("/search", response_model=SearchResponse)
@limiter.limit(RATE_LIMIT_SEARCH)
def search_faq(request: Request, body: SearchRequest, db: Session = Depends(get_db)):
    logger.info(f"Search query: '{body.query}'")
    embedding = get_embedding(body.query)
    result = faq_repo.search_by_embedding(db, embedding)

    if result:
        row, similarity = result
        if similarity >= SIMILARITY_THRESHOLD:
            logger.info(
                f"Match found: similarity={similarity:.3f} "
                f"faq='{row.question}'"
            )
            return SearchResponse(
                found=True,
                question=row.question,
                answer=row.answer,
                category=row.category,
                similarity=similarity
            )
        else:
            # Log the closest miss — useful for threshold tuning
            logger.info(
                f"No match found for query='{body.query}' | "
                f"Closest FAQ: '{row.question}' | "
                f"Similarity: {similarity:.3f} | "
                f"Threshold: {SIMILARITY_THRESHOLD}"
            )
    else:
        logger.info(f"No FAQs in database to search against")

    unanswered_repo.record(db, body.query)
    return SearchResponse(found=False)