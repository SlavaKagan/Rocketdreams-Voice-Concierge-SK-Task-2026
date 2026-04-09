import httpx
import os
import logging
from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    Agent,
    AgentSession,
    function_tool,
)
from livekit.plugins import deepgram, elevenlabs, openai, silero
from app.prompts import SYSTEM_PROMPT

load_dotenv()
logger = logging.getLogger("meridian-agent")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ElevenLabs voice IDs
VOICES = {
    1: "pNInz6obpgDQGcFmaJgB",  # Adam — warm, professional male
    2: "21m00Tcm4TlvDq8ikWAM",  # Rachel — friendly, elegant female
    3: "ErXwobaYiN019PkySvjV",  # Antoni — confident American male
    4: "EXAVITQu4vr4xnSDxMaL",  # Bella — calm, clear female
}

def get_active_voice() -> str:
    try:
        with httpx.Client() as client:
            response = client.get(f"{BACKEND_URL}/api/voices")
            data = response.json()
            voice_id = data.get("active_voice_id", 1)
            return VOICES.get(voice_id, "pNInz6obpgDQGcFmaJgB")
    except Exception as e:
        logger.error(f"Failed to get active voice: {e}")
        return "pNInz6obpgDQGcFmaJgB"


class MeridianAgent(Agent):
    def __init__(self):
        super().__init__(instructions=SYSTEM_PROMPT)

    @function_tool
    async def search_knowledge_base(self, query: str) -> str:
        """
        Search the Meridian knowledge base for answers to guest questions.
        Always call this before answering any question about the property.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/api/search",
                    json={"query": query, "threshold": 0.82},
                    timeout=10.0
                )
                result = response.json()
                if result.get("found"):
                    return result["answer"]
                else:
                    return "NO_MATCH"
        except Exception as e:
            logger.error(f"FAQ search failed: {e}")
            return "NO_MATCH"


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    active_voice = get_active_voice()
    logger.info(f"Active voice: {active_voice}")

    session = AgentSession(
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=elevenlabs.TTS(voice_id=active_voice),
        vad=silero.VAD.load(),
    )

    agent = MeridianAgent()

    await session.start(
        room=ctx.room,
        agent=agent,
    )

    await session.generate_reply(
        instructions="Greet the guest with a warm welcome to The Meridian Casino and Resort."
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))