import logging
from sqlalchemy.orm import Session
from app.models.models import VoiceConfig
from app.core.constants import DEFAULT_VOICE_ID

logger = logging.getLogger("meridian.repository.voice")

def get_config(db: Session) -> VoiceConfig:
    config = db.query(VoiceConfig).first()
    if not config:
        config = VoiceConfig(active_voice_id=DEFAULT_VOICE_ID)
        db.add(config)
        db.commit()
        db.refresh(config)
    return config

def set_active_voice(db: Session, voice_id: int) -> VoiceConfig:
    config = get_config(db)
    config.active_voice_id = voice_id
    db.commit()
    db.refresh(config)
    logger.info(f"Active voice updated to id={voice_id}")
    return config