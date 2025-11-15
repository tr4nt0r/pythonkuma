"""Check for latest Uptime Kuma release."""

from __future__ import annotations

from dataclasses import dataclass

from aiohttp import ClientError, ClientSession
from yarl import URL

from .exceptions import UpdateException

BASE_URL = URL("https://api.github.com/repos/louislam/uptime-kuma")


@dataclass(kw_only=True)
class LatestRelease:
    """Latest release data."""

    tag_name: str
    name: str
    html_url: str
    body: str


class UpdateChecker:
    """Check for Uptime Kuma updates."""

    def __init__(
        self,
        session: ClientSession,
    ) -> None:
        """Initialize Uptime Kuma release checker."""
        self._session = session

    async def latest_release(self) -> LatestRelease:
        """Fetch latest IronOS release."""
        url = BASE_URL / "releases/latest"
        try:
            async with self._session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return LatestRelease(
                    tag_name=data["tag_name"],
                    name=data["name"],
                    html_url=data["html_url"],
                    body=data["body"],
                )
        except ClientError as e:
            msg = "Failed to fetch latest Uptime Kuma release from Github"
            raise UpdateException(msg) from e
        except KeyError as e:
            msg = "Failed to parse latest Uptime Kuma release from Github response"
            raise UpdateException(msg) from e
