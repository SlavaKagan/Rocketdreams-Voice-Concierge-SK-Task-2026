import logging
from fastapi import APIRouter
from livekit.api import AccessToken, VideoGrants
from app.core.config import settings

router = APIRouter(prefix="/api", tags=["Playground"])
logger = logging.getLogger("meridian.routes.playground")

@router.get("/playground/token")
def get_playground_token():
    """Generate a LiveKit access token for the admin playground."""
    token = (
        AccessToken(
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET,
        )
        .with_identity("admin-playground")
        .with_name("Admin")
        .with_grants(
            VideoGrants(
                room_join=True,
                room="meridian-playground",
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )

    logger.info("Generated playground token for admin")
    return {
        "token": token,
        "url": settings.LIVEKIT_URL,
        "room": "meridian-playground",
    }