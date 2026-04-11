import logging
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from datetime import datetime, timezone
from app.models.models import FAQItem

logger = logging.getLogger("meridian.repository.faq")


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: str = None
) -> list[FAQItem]:
    query = db.query(FAQItem).filter(FAQItem.deleted_at.is_(None))
    if category:
        query = query.filter(FAQItem.category.ilike(category))
    return (
        query
        .order_by(FAQItem.category, FAQItem.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_count(db: Session) -> int:
    return db.query(FAQItem).filter(FAQItem.deleted_at.is_(None)).count()


def get_by_id(db: Session, faq_id: int) -> Optional[FAQItem]:
    return (
        db.query(FAQItem)
        .filter(FAQItem.id == faq_id, FAQItem.deleted_at.is_(None))
        .first()
    )


def create(
    db: Session,
    question: str,
    answer: str,
    category: str,
    embedding: list[float]
) -> FAQItem:
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


def update(
    db: Session,
    item: FAQItem,
    question: str = None,
    answer: str = None,
    category: str = None,
    embedding: list[float] = None
) -> FAQItem:
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
    """Soft delete — sets deleted_at timestamp instead of removing the row."""
    item.deleted_at = datetime.now(timezone.utc)
    db.commit()
    logger.info(f"Soft deleted FAQ item id={item.id}")


def restore(db: Session, faq_id: int) -> Optional[FAQItem]:
    """Restore a soft-deleted FAQ item."""
    item = db.query(FAQItem).filter(FAQItem.id == faq_id).first()
    if item and item.deleted_at is not None:
        item.deleted_at = None
        db.commit()
        db.refresh(item)
        logger.info(f"Restored FAQ item id={item.id}")
        return item
    return None


def get_deleted(db: Session) -> list[FAQItem]:
    """Return all soft-deleted FAQ items."""
    return (
        db.query(FAQItem)
        .filter(FAQItem.deleted_at.isnot(None))
        .order_by(FAQItem.deleted_at.desc())
        .all()
    )


def search_by_embedding(db: Session, embedding: list[float]):
    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
    result = db.execute(
        text("""
            SELECT id, question, answer, category,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM faq_items
            WHERE deleted_at IS NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT 1
        """),
        {"embedding": embedding_str}
    ).fetchone()

    if result:
        return result, result.similarity
    return None