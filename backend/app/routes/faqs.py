import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.faq import FAQCreate, FAQUpdate, FAQResponse
from app.services.embedding import get_embedding
from app.repositories import faq as faq_repo

router = APIRouter(prefix="/api", tags=["FAQs"])
logger = logging.getLogger("meridian.routes.faqs")

@router.get("/faqs", response_model=List[FAQResponse])
def get_faqs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return faq_repo.get_all(db, skip=skip, limit=limit)

@router.get("/faqs/count")
def get_faqs_count(db: Session = Depends(get_db)):
    return {"count": faq_repo.get_count(db)}

@router.post("/faqs", response_model=FAQResponse, status_code=201)
def create_faq(body: FAQCreate, db: Session = Depends(get_db)):
    embedding = get_embedding(body.question + " " + body.answer)
    return faq_repo.create(db, body.question, body.answer, body.category, embedding)

@router.put("/faqs/{faq_id}", response_model=FAQResponse)
def update_faq(faq_id: int, body: FAQUpdate, db: Session = Depends(get_db)):
    item = faq_repo.get_by_id(db, faq_id)
    if not item:
        raise HTTPException(status_code=404, detail="FAQ not found")

    new_embedding = None
    if body.question or body.answer:
        q = body.question or item.question
        a = body.answer or item.answer
        new_embedding = get_embedding(q + " " + a)

    return faq_repo.update(db, item, body.question, body.answer, body.category, new_embedding)

@router.delete("/faqs/{faq_id}", status_code=204)
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    item = faq_repo.get_by_id(db, faq_id)
    if not item:
        raise HTTPException(status_code=404, detail="FAQ not found")
    faq_repo.delete(db, item)