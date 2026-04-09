from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.core.database import get_db
from app.models.models import FAQItem
from app.core.config import settings
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding(text: str) -> list:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

@router.get("/faqs")
def get_faqs(db: Session = Depends(get_db)):
    faqs = db.query(FAQItem).all()
    return [
        {
            "id": f.id,
            "question": f.question,
            "answer": f.answer,
            "category": f.category,
            "created_at": f.created_at
        }
        for f in faqs
    ]

@router.post("/faqs")
def create_faq(faq: FAQCreate, db: Session = Depends(get_db)):
    embedding = get_embedding(faq.question + " " + faq.answer)
    item = FAQItem(
        question=faq.question,
        answer=faq.answer,
        category=faq.category,
        embedding=embedding
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "question": item.question, "answer": item.answer}

@router.put("/faqs/{faq_id}")
def update_faq(faq_id: int, faq: FAQUpdate, db: Session = Depends(get_db)):
    item = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="FAQ not found")

    if faq.question:
        item.question = faq.question
    if faq.answer:
        item.answer = faq.answer
    if faq.category:
        item.category = faq.category

    # Re-generate embedding if question or answer changed
    if faq.question or faq.answer:
        item.embedding = get_embedding(item.question + " " + item.answer)

    db.commit()
    return {"id": item.id, "question": item.question, "answer": item.answer}

@router.delete("/faqs/{faq_id}")
def delete_faq(faq_id: int, db: Session = Depends(get_db)):
    item = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="FAQ not found")
    db.delete(item)
    db.commit()
    return {"deleted": True}