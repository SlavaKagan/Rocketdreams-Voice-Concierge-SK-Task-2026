import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobRequest,
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

# ── Logging setup ──────────────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(log_format))

file_handler = TimedRotatingFileHandler(
    filename=LOG_DIR / "meridian-agent.log",
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8",
)
file_handler.suffix = "%Y-%m-%d"
file_handler.setFormatter(logging.Formatter(log_format))

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler],
)

logger = logging.getLogger("meridian.agent")
# ───────────────────────────────────────────────────────────────────────────────

# Track active job — reject duplicates
_active_job_id: str | None = None


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


async def request_fnc(req: JobRequest) -> None:
    """Accept only one job at a time — reject duplicates."""
    global _active_job_id
    if _active_job_id is not None:
        logger.warning(
            f"Rejecting job {req.job.id} — already handling {_active_job_id}"
        )
        await req.reject()
        return
    await req.accept()


async def entrypoint(ctx: JobContext):
    """Main entrypoint for each LiveKit job (one per guest session)."""
    global _active_job_id
    _active_job_id = ctx.job.id
    LOG_DIR.mkdir(exist_ok=True)
    logger.info(f"New session started: room={ctx.room.name}")

    try:
        await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

        active_voice_id = await get_active_voice_id()
        logger.info(f"Using voice: {active_voice_id}")

        try:
            tts = elevenlabs.TTS(voice_id=active_voice_id)
        except Exception as e:
            logger.warning(f"TTS init failed, falling back: {e}")
            tts = elevenlabs.TTS(voice_id=config.DEFAULT_VOICE_ELEVENLABS_ID)

        session = AgentSession(
            stt=deepgram.STT(),
            llm=openai.LLM(model=config.LLM_MODEL),
            tts=tts,
            vad=silero.VAD.load(),
        )

        agent = MeridianAgent()

        await session.start(
            room=ctx.room,
            agent=agent,
        )

        await session.generate_reply(instructions=GREETING)
        logger.info("Agent session ready")

    finally:
        _active_job_id = None
        logger.info("Session ended, ready for new job")


if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        request_fnc=request_fnc,
        num_idle_processes=1,
        load_threshold=1.0,
    ))