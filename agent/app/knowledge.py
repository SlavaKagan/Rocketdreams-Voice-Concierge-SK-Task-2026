import logging
import asyncio
import httpx
from app.config import config
from app.constants import MAX_RETRIES, RETRY_DELAY, HTTP_SEARCH_TIMEOUT, HTTP_VOICE_TIMEOUT

logger = logging.getLogger("meridian.knowledge")


async def search_faq(query: str) -> str:
    """
    Search the Meridian knowledge base for an answer to the guest's query.
    Retries up to MAX_RETRIES times if the backend is temporarily unavailable.
    Returns the answer string if found, or 'NO_MATCH' if not found.
    """
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{config.BACKEND_URL}/api/search",
                    json={
                        "query": query,
                        "threshold": config.SEARCH_THRESHOLD
                    },
                    timeout=HTTP_SEARCH_TIMEOUT
                )
                response.raise_for_status()
                result = response.json()

                if result.get("found"):
                    logger.info(
                        f"FAQ match found for query='{query}' "
                        f"similarity={result.get('similarity', 0):.3f}"
                    )
                    return result["answer"]

                logger.info(f"No FAQ match for query='{query}'")
                return "NO_MATCH"

        except httpx.TimeoutException:
            logger.warning(
                f"FAQ search timed out (attempt {attempt + 1}/{MAX_RETRIES})"
            )
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
        except httpx.ConnectError:
            logger.warning(
                f"Backend unreachable (attempt {attempt + 1}/{MAX_RETRIES}) "
                f"url={config.BACKEND_URL}"
            )
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"FAQ search failed: {e}")
            return "NO_MATCH"

    logger.error(f"FAQ search failed after {MAX_RETRIES} attempts")
    return "NO_MATCH"


async def get_active_voice_id() -> str:
    """
    Fetch the currently active ElevenLabs voice ID from the backend.
    Retries up to MAX_RETRIES times. Falls back to default if unavailable.
    """
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{config.BACKEND_URL}/api/voices",
                    timeout=HTTP_VOICE_TIMEOUT
                )
                response.raise_for_status()
                data = response.json()
                voice_key = data.get("active_voice_id", 1)
                voice_id = config.VOICES.get(
                    voice_key,
                    config.DEFAULT_VOICE_ELEVENLABS_ID
                )
                logger.info(
                    f"Active voice: key={voice_key} elevenlabs_id={voice_id}"
                )
                return voice_id

        except httpx.ConnectError:
            logger.warning(
                f"Backend unreachable for voice config "
                f"(attempt {attempt + 1}/{MAX_RETRIES})"
            )
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)
        except Exception as e:
            logger.error(f"Failed to fetch active voice: {e}")
            break

    logger.warning("Using default voice due to backend unavailability")
    return config.DEFAULT_VOICE_ELEVENLABS_ID