from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.models import VoiceConfig

router = APIRouter()

VOICES = {
    1: {"id": 1, "name": "James", "description": "Male, mature, warm British accent. Professional and refined."},
    2: {"id": 2, "name": "Sofia", "description": "Female, friendly, subtle European accent. Welcoming and elegant."},
    3: {"id": 3, "name": "Marcus", "description": "Male, American, confident and energetic. Modern and approachable."},
    4: {"id": 4, "name": "Elena", "description": "Female, American, calm and reassuring. Sophisticated and clear."},
}

class VoiceUpdate(BaseModel):
    voice_id: int

@router.get("/voices")
def get_voices(db: Session = Depends(get_db)):
    config = db.query(VoiceConfig).first()
    active_id = config.active_voice_id if config else 1
    return {
        "active_voice_id": active_id,
        "voices": list(VOICES.values())
    }

@router.put("/voices/active")
def set_active_voice(body: VoiceUpdate, db: Session = Depends(get_db)):
    if body.voice_id not in VOICES:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid voice ID")
    config = db.query(VoiceConfig).first()
    if config:
        config.active_voice_id = body.voice_id
    else:
        config = VoiceConfig(active_voice_id=body.voice_id)
        db.add(config)
    db.commit()
    return {"active_voice_id": body.voice_id}