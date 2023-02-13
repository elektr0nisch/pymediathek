import asyncio
import aiohttp

import pymediathek
from pymediathek import MediathekOptions


async def main():
    """Run with aiohttp ClientSession."""
    async with aiohttp.ClientSession() as session:
        await run(session)


async def run(session):
    """Use library."""

    result = await pymediathek.resolve_video_url(
        website_url="https://www.ardmediathek.de/video/Y3JpZDovL3dkci5kZS9CZWl0cmFnLWNlZjM1NGFjLTU0ZTctNGRjZS04ZGUwLTc4MjBjMjFhYjc4Yw",
        options=MediathekOptions(
            workingDirectory="C:\\test", httpSession=session
        ),
    )

    print(result)


asyncio.run(main())
