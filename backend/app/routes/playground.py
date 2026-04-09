import logging
from fastapi import APIRouter
from livekit.api import AccessToken, VideoGrants, LiveKitAPI, CreateAgentDispatchRequest
from app.core.config import settings
from app.core.constants import PLAYGROUND_ROOM

router = APIRouter(prefix="/api", tags=["Playground"])
logger = logging.getLogger("meridian.routes.playground")

@router.get("/playground/token")
async def get_playground_token():
    """Generate a LiveKit access token and dispatch agent for the admin playground."""
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
                room=PLAYGROUND_ROOM,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .to_jwt()
    )

    try:
        async with LiveKitAPI(
            url=settings.LIVEKIT_URL,
            api_key=settings.LIVEKIT_API_KEY,
            api_secret=settings.LIVEKIT_API_SECRET,
        ) as lk:
            await lk.agent_dispatch.create_dispatch(
                CreateAgentDispatchRequest(
                    room=PLAYGROUND_ROOM,
                    agent_name="",
                )
            )
            logger.info(f"Agent dispatched to room: {PLAYGROUND_ROOM}")
    except Exception as e:
        logger.warning(f"Agent dispatch failed: {e}")

    logger.info("Generated playground token for admin")
    return {
        "token": token,
        "url": settings.LIVEKIT_URL,
        "room": PLAYGROUND_ROOM,
    }