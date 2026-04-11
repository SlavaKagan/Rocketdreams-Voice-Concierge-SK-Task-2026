import logging
import asyncio
from fastapi import APIRouter
from livekit.api import (
    AccessToken,
    VideoGrants,
    LiveKitAPI,
    CreateAgentDispatchRequest,
)
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

    async with LiveKitAPI(
        url=settings.LIVEKIT_URL,
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET,
    ) as lk:
        # Step 1 — delete existing dispatches
        try:
            dispatches = await lk.agent_dispatch.list_dispatch(
                room_name=PLAYGROUND_ROOM
            )
            logger.info(f"Found {len(dispatches)} existing dispatches")
            for dispatch in dispatches:
                try:
                    await lk.agent_dispatch.delete_dispatch(
                        dispatch_id=dispatch.id,
                        room_name=PLAYGROUND_ROOM,
                    )
                    logger.info(f"Deleted dispatch: {dispatch.id}")
                except Exception as e:
                    logger.warning(f"Failed to delete dispatch {dispatch.id}: {e}")
        except Exception as e:
            logger.warning(f"No existing dispatches (room may not exist): {e}")

        # Step 2 — delete room
        try:
            await lk.room.delete_room(room=PLAYGROUND_ROOM)
            logger.info(f"Deleted room: {PLAYGROUND_ROOM}")
            await asyncio.sleep(1)
        except Exception:
            pass

        # Step 3 — single dispatch
        try:
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