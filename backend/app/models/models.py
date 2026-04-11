from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class FAQItem(Base):
    __tablename__ = "faq_items"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    embedding = Column(Vector(1536), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)  # None = active, set = soft deleted


class UnansweredQuestion(Base):
    __tablename__ = "unanswered_questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    frequency = Column(Integer, default=1)
    dismissed = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    last_asked_at = Column(DateTime, server_default=func.now())


class VoiceConfig(Base):
    __tablename__ = "voice_config"

    id = Column(Integer, primary_key=True, index=True)
    active_voice_id = Column(Integer, default=1)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())