from pydantic import BaseModel
from typing import List

class VoiceOption(BaseModel):
    id: int
    name: str
    elevenlabs_id: str
    description: str

class VoicesResponse(BaseModel):
    active_voice_id: int
    voices: List[VoiceOption]

class VoiceUpdateRequest(BaseModel):
    voice_id: int