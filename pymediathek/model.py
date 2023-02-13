"""Models for pymediathek."""
import aiohttp
import json

from dataclasses import dataclass

@dataclass
class MediathekOptions:
    """Options for pymediathek."""

    workingDirectory: str
    httpSession: aiohttp.ClientSession

@dataclass
class MediathekProgramme:
    """Entry in the Mediathek."""

    channel: str
    topic: str
    title: str
    website_url: str
    video_url: str