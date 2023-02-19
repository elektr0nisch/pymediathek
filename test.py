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

    result = await pymediathek.find_programme(
        field="website_url",
        target_value="https://www.ardmediathek.de/video/ndr-dokfilm/schockwellen-nachrichten-aus-der-pandemie/ndr/Y3JpZDovL25kci5kZS9wcm9wbGFuXzE5NjMxNTc3MF9nYW56ZVNlbmR1bmc",
        options=MediathekOptions(
            working_directory="C:\\test", http_session=session
        ),
    )

    print(result)


asyncio.run(main())
