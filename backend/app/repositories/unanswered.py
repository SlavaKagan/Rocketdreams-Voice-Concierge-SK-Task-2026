import logging
from sqlalchemy.orm import Session
from typing import Optional
from app.models.models import UnansweredQuestion

logger = logging.getLogger("meridian.repository.unanswered")

def get_all_active(db: Session, skip: int = 0, limit: int = 100) -> list[UnansweredQuestion]:
    return (
        db.query(UnansweredQuestion)
        .filter(UnansweredQuestion.dismissed == 0)
        .order_by(UnansweredQuestion.frequency.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_count(db: Session) -> int:
    return (
        db.query(UnansweredQuestion)
        .filter(UnansweredQuestion.dismissed == 0)
        .count()
    )

def get_by_id(db: Session, question_id: int) -> Optional[UnansweredQuestion]:
    return db.query(UnansweredQuestion).filter(UnansweredQuestion.id == question_id).first()

def find_active_by_text(db: Session, question: str) -> Optional[UnansweredQuestion]:
    return (
        db.query(UnansweredQuestion)
        .filter(
            UnansweredQuestion.question == question,
            UnansweredQuestion.dismissed == 0
        )
        .first()
    )

def record(db: Session, question: str) -> UnansweredQuestion:
    existing = find_active_by_text(db, question)
    if existing:
        existing.frequency += 1
        db.commit()
        logger.info(f"Incremented frequency for unanswered question id={existing.id} freq={existing.frequency}")
        return existing

    item = UnansweredQuestion(question=question)
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"Recorded new unanswered question id={item.id}")
    return item

def dismiss(db: Session, item: UnansweredQuestion) -> None:
    item.dismissed = 1
    db.commit()
    logger.info(f"Dismissed unanswered question id={item.id}")

def delete(db: Session, item: UnansweredQuestion) -> None:
    db.delete(item)
    db.commit()