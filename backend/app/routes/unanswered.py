import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.unanswered import UnansweredResponse, ConvertToFAQRequest
from app.services.embedding import get_embedding
from app.repositories import unanswered as unanswered_repo
from app.repositories import faq as faq_repo

router = APIRouter(prefix="/api", tags=["Unanswered Questions"])
logger = logging.getLogger("meridian.routes.unanswered")

@router.get("/unanswered", response_model=List[UnansweredResponse])
def get_unanswered(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return unanswered_repo.get_all_active(db, skip=skip, limit=limit)

@router.get("/unanswered/count")
def get_unanswered_count(db: Session = Depends(get_db)):
    return {"count": unanswered_repo.get_count(db)}

@router.post("/unanswered/{question_id}/convert", response_model=dict)
def convert_to_faq(question_id: int, body: ConvertToFAQRequest, db: Session = Depends(get_db)):
    item = unanswered_repo.get_by_id(db, question_id)
    if not item:
        raise HTTPException(status_code=404, detail="Question not found")

    embedding = get_embedding(item.question + " " + body.answer)
    faq = faq_repo.create(db, item.question, body.answer, body.category, embedding)
    unanswered_repo.delete(db, item)

    logger.info(f"Converted unanswered question id={question_id} to FAQ id={faq.id}")
    return {"converted": True, "faq_id": faq.id}

@router.delete("/unanswered/{question_id}/dismiss", status_code=204)
def dismiss_question(question_id: int, db: Session = Depends(get_db)):
    item = unanswered_repo.get_by_id(db, question_id)
    if not item:
        raise HTTPException(status_code=404, detail="Question not found")
    unanswered_repo.dismiss(db, item)