import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.models.models import FAQItem

logger = logging.getLogger("meridian.repository.faq")

def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[FAQItem]:
    return (
        db.query(FAQItem)
        .order_by(FAQItem.category, FAQItem.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_count(db: Session) -> int:
    return db.query(FAQItem).count()

def get_by_id(db: Session, faq_id: int) -> Optional[FAQItem]:
    return db.query(FAQItem).filter(FAQItem.id == faq_id).first()

def create(db: Session, question: str, answer: str, category: str, embedding: list[float]) -> FAQItem:
    item = FAQItem(
        question=question,
        answer=answer,
        category=category,
        embedding=embedding
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"Created FAQ item id={item.id} category={category}")
    return item

def update(db: Session, item: FAQItem, question: str = None, answer: str = None, category: str = None, embedding: list[float] = None) -> FAQItem:
    if question is not None:
        item.question = question
    if answer is not None:
        item.answer = answer
    if category is not None:
        item.category = category
    if embedding is not None:
        item.embedding = embedding
    db.commit()
    db.refresh(item)
    logger.info(f"Updated FAQ item id={item.id}")
    return item

def delete(db: Session, item: FAQItem) -> None:
    db.delete(item)
    db.commit()
    logger.info(f"Deleted FAQ item id={item.id}")

def search_by_embedding(db: Session, embedding: list[float]):
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

    if result:
        return result, result.similarity
    return None