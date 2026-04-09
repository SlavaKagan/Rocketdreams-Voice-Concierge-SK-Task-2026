import logging
import httpx
from app.config import config

logger = logging.getLogger("meridian.knowledge")

async def search_faq(query: str) -> str:
    """
    Search the Meridian knowledge base for an answer to the guest's query.
    Returns the answer string if found, or 'NO_MATCH' if not found.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.BACKEND_URL}/api/search",
                json={
                    "query": query,
                    "threshold": config.SEARCH_THRESHOLD
                },
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            if result.get("found"):
                logger.info(f"FAQ match found for query='{query}' similarity={result.get('similarity', 0):.3f}")
                return result["answer"]

            logger.info(f"No FAQ match for query='{query}'")
            return "NO_MATCH"

    except httpx.TimeoutException:
        logger.error(f"FAQ search timed out for query='{query}'")
        return "NO_MATCH"
    except Exception as e:
        logger.error(f"FAQ search failed: {e}")
        return "NO_MATCH"


def get_active_voice_id() -> str:
    """
    Fetch the currently active ElevenLabs voice ID from the backend.
    Falls back to default if unavailable.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{config.BACKEND_URL}/api/voices",
                timeout=5.0
            )
            response.raise_for_status()
            data = response.json()
            voice_key = data.get("active_voice_id", 1)
            voice_id = config.VOICES.get(voice_key, config.DEFAULT_VOICE_ELEVENLABS_ID)
            logger.info(f"Active voice: key={voice_key} elevenlabs_id={voice_id}")
            return voice_id
    except Exception as e:
        logger.error(f"Failed to fetch active voice, using default: {e}")
        return config.DEFAULT_VOICE_ELEVENLABS_ID