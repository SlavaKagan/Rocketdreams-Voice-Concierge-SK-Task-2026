from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import UnansweredQuestion, FAQItem
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

class ConvertToFAQ(BaseModel):
    answer: str
    category: str = "General"

@router.get("/unanswered")
def get_unanswered(db: Session = Depends(get_db)):
    questions = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.dismissed == 0
    ).order_by(UnansweredQuestion.frequency.desc()).all()
    return [
        {
            "id": q.id,
            "question": q.question,
            "frequency": q.frequency,
            "created_at": q.created_at,
            "last_asked_at": q.last_asked_at
        }
        for q in questions
    ]

@router.post("/unanswered/{question_id}/convert")
def convert_to_faq(question_id: int, body: ConvertToFAQ, db: Session = Depends(get_db)):
    question = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    embedding = get_embedding(question.question + " " + body.answer)
    faq = FAQItem(
        question=question.question,
        answer=body.answer,
        category=body.category,
        embedding=embedding
    )
    db.add(faq)
    db.delete(question)
    db.commit()
    return {"converted": True, "faq_id": faq.id}

@router.delete("/unanswered/{question_id}/dismiss")
def dismiss_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.id == question_id
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.dismissed = 1
    db.commit()
    return {"dismissed": True}