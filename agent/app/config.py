import os
from dotenv import load_dotenv

load_dotenv()

class AgentConfig:
    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    LLM_MODEL: str = "gpt-4o"
    SEARCH_THRESHOLD: float = 0.82

    # ElevenLabs voice IDs mapped to our 4 voice options
    VOICES: dict = {
        1: "pNInz6obpgDQGcFmaJgB",  # James — warm British male
        2: "21m00Tcm4TlvDq8ikWAM",  # Sofia — elegant European female
        3: "ErXwobaYiN019PkySvjV",  # Marcus — confident American male
        4: "EXAVITQu4vr4xnSDxMaL",  # Elena — calm American female
    }
    DEFAULT_VOICE_ELEVENLABS_ID: str = "pNInz6obpgDQGcFmaJgB"

config = AgentConfig()