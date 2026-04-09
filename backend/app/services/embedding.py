import logging
import time
from openai import OpenAI
from app.core.config import settings
from app.core.constants import EMBEDDING_MODEL

logger = logging.getLogger("meridian.embedding")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding(text: str, retries: int = 3) -> list[float]:
    """Generate an embedding vector for the given text with retry logic."""
    for attempt in range(retries):
        try:
            response = client.embeddings.create(
                input=text,
                model=EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Embedding failed after {retries} attempts: {e}")
                raise
            logger.warning(f"Embedding attempt {attempt + 1} failed, retrying in 1s: {e}")
            time.sleep(1)
    raise RuntimeError("Embedding failed")