# PyMediathek

Python library for [MediathekView](https://mediathekview.de/)

## Requirements

- Python >= 3.10
- aiohttp

## Known issue with `website_url`

As there are many merley independent tv organisations in germany, austria and switzerland, this library currently doesn't support all possible values for `website_url`. If you encounter such a problem, feel free to create a pull request with your solution or just create an issue and I'll take a look at it!

*E.g. to make `ardmediathek.de` work out-of-the-box I had to truncate everything between `/video` and the actual video id (see example below)* 

## Install
```bash
pip install pymediathek
```

## Example

```python
from pymediathek import MediathekOptions, find_programme

import asyncio
import aiohttp

async def main():
    """Run with aiohttp ClientSession."""
    async with aiohttp.ClientSession() as session:
        await run(session)


async def run(session):
    """Use library."""
    programme = await find_programme(
        field="website_url",
        target_value="https://www.ardmediathek.de/video/ndr-dokfilm/schockwellen-nachrichten-aus-der-pandemie/ndr/Y3JpZDovL25kci5kZS9wcm9wbGFuXzE5NjMxNTc3MF9nYW56ZVNlbmR1bmc",
        options=MediathekOptions(working_directory="C:\\test", http_session=session),
    )

    print(programme)


asyncio.run(main())
```

This returns the following result (where `video_url` would be the downloadable video):

```bash
{'channel': '', 'topic': '', 'title': 'Schockwellen - Nachrichten aus der Pandemie', 'website_url': 'https://www.ardmediathek.de/video/Y3JpZDovL25kci5kZS9wcm9wbGFuXzE5NjMxNTc3MF9nYW56ZVNlbmR1bmc', 'video_url': 'https://mediandr-a.akamaihd.net/progressive_geo/2023/0213/TV-20230213-1209-1200.hq.hevc.mp4'}
```

## Credits

Special thanks to the contributors of MediathekView and MediathekViewWeb. Without it, this library simply wouldn't exist.
