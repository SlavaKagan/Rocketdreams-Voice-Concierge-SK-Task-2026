from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    # Database
    DATABASE_URL: str

    # OpenAI
    OPENAI_API_KEY: str

    # LiveKit
    LIVEKIT_URL: str = ""
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""

    # ElevenLabs
    ELEVENLABS_API_KEY: str = ""

    # Deepgram
    DEEPGRAM_API_KEY: str = ""

settings = Settings()