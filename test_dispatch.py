import asyncio
import os
from livekit.api import LiveKitAPI, agent_dispatch_service
import inspect

async def main():
    async with LiveKitAPI(
        url=os.environ['LIVEKIT_URL'],
        api_key=os.environ['LIVEKIT_API_KEY'],
        api_secret=os.environ['LIVEKIT_API_SECRET'],
    ) as lk:
        print(inspect.signature(lk.agent_dispatch.create_dispatch))
        print(inspect.signature(lk.agent_dispatch.list_dispatch))
        print(inspect.signature(lk.agent_dispatch.delete_dispatch))

asyncio.run(main())