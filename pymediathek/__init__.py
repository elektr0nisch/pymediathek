"""Python library for MediathekView."""
import os
import aiofiles
import lzma
import re
import json
import logging

from datetime import datetime
from urllib.parse import urlparse

from .model import MediathekOptions, MediathekProgramme
from .const import (
    CONTENT_LIST_URL,
    COMPRESSED_CONTENT_LIST_FILENAME,
    CONTENT_LIST_FILENAME,
    PROGRAMME_FIELD_WEBSITE_URL
)

programmes: list[MediathekProgramme] = []


async def find_programme(
    field: str, target_value: str, options: MediathekOptions
) -> str:
    await _init(options)

    # Ensure caseless comparsion 
    target_value = target_value.casefold()

    # Modify input value to improve matching
    if field == PROGRAMME_FIELD_WEBSITE_URL:
        website_url = urlparse(target_value)

        # Special conditions for website URLs from ardmediathek.de
        if website_url.hostname.__contains__("ardmediathek.de"):
            path_parts = website_url.path[1::].split("/")

            # Remove garbage between "/video" and the video id
            if len(path_parts) > 2:
                website_url = website_url._replace(path=path_parts[0] + "/" + path_parts[-1])
                target_value = website_url.geturl()

    # Find programme according to input value
    for programme in programmes:
        attribute: str = programme[field]
        if attribute and attribute.casefold() == target_value:
            return programme


async def _init(options: MediathekOptions) -> None:
    os.makedirs(options.working_directory, exist_ok=True)

    content_list = os.path.join(options.working_directory, CONTENT_LIST_FILENAME)
    if os.path.exists(content_list):
        last_modified = os.path.getmtime(content_list)
        delta = datetime.now() - datetime.fromtimestamp(last_modified)

        # If content file isn't older than 24 hours don't download
        if delta.total_seconds() < 86400:
            await _loadList(content_list)
            return

    await _downloadList(options)


async def _loadList(content_list: str):
    with open(content_list, "r") as file:
        global programmes
        programmes = json.load(file)

async def _downloadList(options: MediathekOptions):
    compressed_content_list = os.path.join(
        options.working_directory, COMPRESSED_CONTENT_LIST_FILENAME
    )
    content_list = os.path.join(options.working_directory, CONTENT_LIST_FILENAME)

    # Download content list
    async with options.http_session as session:
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

        jsonObjects = []
        for line in lines:
            if line:
                try:
                    object = json.loads(line)

                    # Construct programme object with the fields position in the json array
                    programme = MediathekProgramme(
                        object[0], object[1], object[2], object[9], object[8]
                    )

                    # Add programmes read to correct lists
                    programmes.append(programme)
                    jsonObjects.append(programme.__dict__)
                except json.JSONDecodeError as e:
                    logging.exception(e)

    with open(content_list, "w", encoding="utf-8") as file:
        file.write(json.dumps(jsonObjects, indent=4))

    # Remove compressed list
    os.remove(compressed_content_list)
