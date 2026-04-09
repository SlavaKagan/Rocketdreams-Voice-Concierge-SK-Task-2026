import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.constants import VOICES
from app.schemas.voice import VoicesResponse, VoiceOption, VoiceUpdateRequest
from app.repositories import voice as voice_repo

router = APIRouter(prefix="/api", tags=["Voice"])
logger = logging.getLogger("meridian.routes.voice")

@router.get("/voices", response_model=VoicesResponse)
def get_voices(db: Session = Depends(get_db)):
    config = voice_repo.get_config(db)
    return VoicesResponse(
        active_voice_id=config.active_voice_id,
        voices=[VoiceOption(**v) for v in VOICES.values()]
    )

@router.put("/voices/active", response_model=dict)
def set_active_voice(body: VoiceUpdateRequest, db: Session = Depends(get_db)):
    if body.voice_id not in VOICES:
        raise HTTPException(status_code=400, detail=f"Invalid voice ID. Must be one of: {list(VOICES.keys())}")
    config = voice_repo.set_active_voice(db, body.voice_id)
    return {"active_voice_id": config.active_voice_id}