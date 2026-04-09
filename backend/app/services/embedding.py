import logging
from openai import OpenAI
from app.core.config import settings
from app.core.constants import EMBEDDING_MODEL

logger = logging.getLogger("meridian.embedding")

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding(text: str) -> list[float]:
    """Generate an embedding vector for the given text."""
    try:
        response = client.embeddings.create(
            input=text,
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        raise