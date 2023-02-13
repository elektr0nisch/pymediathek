"""Python library for MediathekView."""
import os
import aiofiles
import lzma
import re
import json

from datetime import datetime

from .model import MediathekOptions, MediathekProgramme
from .const import (
    CONTENT_LIST_URL,
    COMPRESSED_CONTENT_LIST_FILENAME,
    CONTENT_LIST_FILENAME,
)

programmes: list[MediathekProgramme] = []


async def resolve_video_url(website_url: str, options: MediathekOptions) -> str:
    await _init(options)

    for programme in programmes:
        if programme.website_url == website_url:
            return programme.video_url


async def _init(options: MediathekOptions) -> None:
    os.makedirs(options.workingDirectory, exist_ok=True)

    content_list = os.path.join(options.workingDirectory, CONTENT_LIST_FILENAME)
    download = True
    if os.path.exists(content_list):
        last_modified = os.path.getmtime(content_list)
        delta = datetime.now() - datetime.fromtimestamp(last_modified)

        # If content file isn't older than 24 hours don't download
        if delta.total_seconds() < 86400:
            print("load")
            await _loadList(content_list)
            return

    await _downloadList(options)


async def _loadList(content_list: str):
    with open(content_list, "r") as file:
        programmes = json.load(file)


async def _downloadList(options: MediathekOptions):
    compressed_content_list = os.path.join(
        options.workingDirectory, COMPRESSED_CONTENT_LIST_FILENAME
    )
    content_list = os.path.join(options.workingDirectory, CONTENT_LIST_FILENAME)

    # Download content list
    async with options.httpSession as session:
        async with session.get(CONTENT_LIST_URL) as response:
            if not response.status == 200:
                raise RuntimeError("invalid response")

            data = await response.read()

        async with aiofiles.open(compressed_content_list, "wb") as file:
            await file.write(data)

    # Unpack content list
    with lzma.open(compressed_content_list) as compressed:
        raw = compressed.readline().decode("utf-8")
        lines = re.compile('^{"Filmliste":|,"X":|}$').split(raw)

        for line in lines:
            if line: 
                try:
                    object = json.loads(line)
                    programmes.append(
                        MediathekProgramme(object[0], object[1], object[3], object[9], object[8])
                    )
                except Exception as e:
                    print(e.__str__)
                
    print(programmes[0])

    objects = []
    for programme in programmes:
        objects.append(programme.__dict__)

    with open(content_list, "w", encoding="utf-8") as file:
        file.write(json.dumps(objects, indent=4))

    # Remove compressed list
    os.remove(compressed_content_list)
