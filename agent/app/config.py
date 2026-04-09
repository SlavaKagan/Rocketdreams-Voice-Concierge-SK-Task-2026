from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class AgentSettings(BaseSettings):
    LIVEKIT_URL: str = ""
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    OPENAI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    DEEPGRAM_API_KEY: str = ""
    BACKEND_URL: str = "http://localhost:8000"
    LLM_MODEL: str = "gpt-4o"
    SEARCH_THRESHOLD: float = 0.82
    DEFAULT_VOICE_ELEVENLABS_ID: str = "pNInz6obpgDQGcFmaJgB"

    VOICES: dict = {
        1: "pNInz6obpgDQGcFmaJgB",  # James
        2: "21m00Tcm4TlvDq8ikWAM",  # Sofia
        3: "ErXwobaYiN019PkySvjV",  # Marcus
        4: "EXAVITQu4vr4xnSDxMaL",  # Elena
    }

    class Config:
        env_file = ".env"

config = AgentSettings()