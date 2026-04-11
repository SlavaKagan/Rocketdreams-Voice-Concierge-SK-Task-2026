from pydantic_settings import BaseSettings
from pydantic import ConfigDict, model_validator
from dotenv import load_dotenv

load_dotenv()

class AgentSettings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

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
        2: "SUt4lKV5Yg2QPF7Bs3Ae",  # Sofia
        3: "ErXwobaYiN019PkySvjV",  # Marcus
        4: "EXAVITQu4vr4xnSDxMaL",  # Elena
    }

    @model_validator(mode="after")
    def validate_required(self) -> "AgentSettings":
        required = {
            "LIVEKIT_URL": self.LIVEKIT_URL,
            "LIVEKIT_API_KEY": self.LIVEKIT_API_KEY,
            "LIVEKIT_API_SECRET": self.LIVEKIT_API_SECRET,
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
            "ELEVENLABS_API_KEY": self.ELEVENLABS_API_KEY,
            "DEEPGRAM_API_KEY": self.DEEPGRAM_API_KEY,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        return self

config = AgentSettings()