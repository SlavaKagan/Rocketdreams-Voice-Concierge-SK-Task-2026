from pydantic_settings import BaseSettings
from pydantic import ConfigDict, model_validator

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    # Database
    DATABASE_URL: str = ""

    # OpenAI
    OPENAI_API_KEY: str = ""

    # LiveKit
    LIVEKIT_URL: str = ""
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""

    # ElevenLabs
    ELEVENLABS_API_KEY: str = ""

    # Deepgram
    DEEPGRAM_API_KEY: str = ""

    @model_validator(mode="after")
    def validate_required(self) -> "Settings":
        # Only these two are required for all services including seeder
        required = {
            "DATABASE_URL": self.DATABASE_URL,
            "OPENAI_API_KEY": self.OPENAI_API_KEY,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )
        return self

settings = Settings()