from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import FAQItem, UnansweredQuestion
from app.core.config import settings
from openai import OpenAI

router = APIRouter()
client = OpenAI(api_key=settings.OPENAI_API_KEY)

class SearchRequest(BaseModel):
    query: str
    threshold: float = 0.82

def get_embedding(text_input: str) -> list:
    response = client.embeddings.create(
        input=text_input,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

@router.post("/search")
def search_faq(request: SearchRequest, db: Session = Depends(get_db)):
    embedding = get_embedding(request.query)
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    result = db.execute(
        text("""
            SELECT id, question, answer, category,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM faq_items
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT 1
        """),
        {"embedding": embedding_str}
    ).fetchone()

    if result and result.similarity >= request.threshold:
        return {
            "found": True,
            "question": result.question,
            "answer": result.answer,
            "category": result.category,
            "similarity": result.similarity
        }

    # No match — record as unanswered
    existing = db.query(UnansweredQuestion).filter(
        UnansweredQuestion.question == request.query,
        UnansweredQuestion.dismissed == 0
    ).first()

    if existing:
        existing.frequency += 1
        db.commit()
    else:
        unanswered = UnansweredQuestion(question=request.query)
        db.add(unanswered)
        db.commit()

    return {"found": False}