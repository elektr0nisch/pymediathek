"""Models for pymediathek."""
import aiohttp

from dataclasses import dataclass

@dataclass
class MediathekOptions:
    """Options for pymediathek."""

    working_directory: str
    http_session: aiohttp.ClientSession

@dataclass
class MediathekProgramme:
    """Entry in the Mediathek."""

    channel: str
    topic: str
    title: str
    website_url: str
    video_url: str