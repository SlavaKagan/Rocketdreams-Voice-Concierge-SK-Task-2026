import logging
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from elevenlabs import ElevenLabs
from app.core.database import get_db
from app.core.constants import VOICES, VOICE_PREVIEW_TEXT, ELEVENLABS_TTS_MODEL
from app.core.config import settings
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
        raise HTTPException(
            status_code=400,
            detail=f"Invalid voice ID. Must be one of: {list(VOICES.keys())}"
        )
    config = voice_repo.set_active_voice(db, body.voice_id)
    return {"active_voice_id": config.active_voice_id}


@router.get("/voices/{voice_id}/preview")
def preview_voice(voice_id: int):
    """Generate a short TTS audio preview for a given voice."""
    if voice_id not in VOICES:
        raise HTTPException(status_code=404, detail="Voice not found")

    voice = VOICES[voice_id]
    elevenlabs_id = voice["elevenlabs_id"]

    try:
        client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        audio = client.text_to_speech.convert(
            voice_id=elevenlabs_id,
            text=VOICE_PREVIEW_TEXT,
            model_id=ELEVENLABS_TTS_MODEL,
        )
        audio_bytes = b"".join(audio)
        logger.info(f"Generated voice preview for voice_id={voice_id} name={voice['name']}")
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"inline; filename=preview_{voice_id}.mp3"}
        )
    except Exception as e:
        logger.error(f"Voice preview failed for voice_id={voice_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate voice preview")