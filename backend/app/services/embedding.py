import logging
import time
import hashlib
from openai import OpenAI
from app.core.config import settings
from app.core.constants import EMBEDDING_MODEL

logger = logging.getLogger("meridian.embedding")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# In-memory cache — persists for lifetime of the process
_embedding_cache: dict[str, list[float]] = {}

def get_embedding(text: str, retries: int = 3) -> list[float]:
    """
    Generate an embedding vector for the given text.
    Results are cached by text hash to avoid duplicate OpenAI API calls.
    """
    # Normalize and hash the text for cache key
    normalized = text.lower().strip()
    cache_key = hashlib.md5(normalized.encode()).hexdigest()

    if cache_key in _embedding_cache:
        logger.debug(f"Embedding cache hit for: '{text[:50]}'")
        return _embedding_cache[cache_key]

    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                input=normalized,
                model=EMBEDDING_MODEL
            )
            embedding = response.data[0].embedding
            _embedding_cache[cache_key] = embedding
            logger.debug(f"Embedding generated and cached for: '{text[:50]}'")
            return embedding
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Embedding failed after {retries} attempts: {e}")
                raise
            logger.warning(f"Embedding attempt {attempt + 1} failed, retrying in 1s: {e}")
            time.sleep(1)

    raise RuntimeError("Embedding generation failed")

def get_cache_stats() -> dict:
    """Return current cache statistics."""
    return {
        "cached_embeddings": len(_embedding_cache),
    }