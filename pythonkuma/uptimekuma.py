"""Uptime Kuma client."""

from aiohttp import ClientSession
from yarl import URL

from .decorator import api_request
from .models import UptimeKumaApiResponse


class UptimeKuma:
    """This class is used to get information from Uptime Kuma."""

    def __init__(self, session: ClientSession, base_url: URL | str, username: str, password: str) -> None:
        """Initialize"""
        self.monitors = []
        self._base_url = base_url if isinstance(base_url, URL) else URL(base_url)
        self._username = username
        self._password = password
        self._session: ClientSession = session

    @api_request("metrics")
    async def async_get_monitors(self, **kwargs) -> UptimeKumaApiResponse:
        """Get monitors from API."""
