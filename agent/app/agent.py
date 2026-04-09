import logging
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
from app.config import config
from app.knowledge import search_faq, get_active_voice_id
from app.prompts import SYSTEM_PROMPT, GREETING

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("meridian.agent")


class MeridianAgent(Agent):
    """
    Voice concierge agent for The Meridian Casino & Resort.
    Handles guest queries by searching the property knowledge base
    and responding naturally via voice.
    """

    def __init__(self):
        super().__init__(instructions=SYSTEM_PROMPT)

    @function_tool
    async def search_knowledge_base(self, query: str) -> str:
        """
        Search the Meridian property knowledge base.
        Call this for every guest question about the property
        before formulating a response.

        Args:
            query: The guest's question or topic to search for.

        Returns:
            The answer from the knowledge base, or NO_MATCH if not found.
        """
        return await search_faq(query)


async def entrypoint(ctx: JobContext):
    """Main entrypoint for each LiveKit job (one per guest session)."""
    logger.info(f"New session started: room={ctx.room.name}")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    active_voice_id = get_active_voice_id()

    session = AgentSession(
        stt=deepgram.STT(),
        llm=openai.LLM(model=config.LLM_MODEL),
        tts=elevenlabs.TTS(voice_id=active_voice_id),
        vad=silero.VAD.load(),
    )

    agent = MeridianAgent()

    await session.start(
        room=ctx.room,
        agent=agent,
    )

    await session.generate_reply(instructions=GREETING)

    logger.info("Agent session ready")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))