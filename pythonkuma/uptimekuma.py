"""Uptime Kuma client."""

from http import HTTPStatus
from typing import Any

from aiohttp import (
    BasicAuth,
    ClientError,
    ClientResponseError,
    ClientSession,
    ClientTimeout,
)
from prometheus_client.parser import text_string_to_metric_families
from yarl import URL

from .exceptions import UptimeKumaAuthenticationException, UptimeKumaConnectionException
from .models import UptimeKumaMonitor, UptimeKumaVersion


class UptimeKuma:
    """Uptime Kuma client."""

    def __init__(
        self,
        session: ClientSession,
        base_url: URL | str,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Initialize the Uptime Kuma client.

        Parameters
        ----------
        session : ClientSession
            An aiohttp ClientSession instance
        base_url : URL or str
            The base URL of the Uptime Kuma server
        api_key : str or None, optional
            API key for authentication (default is None).
        timeout : float or None, optional
            Request timeout in seconds (default is 10 seconds if not specified).
        """
        self._base_url = base_url if isinstance(base_url, URL) else URL(base_url)

        self._auth = BasicAuth("", api_key) if api_key else None

        self._timeout = ClientTimeout(total=timeout or 10)
        self._session = session

        self.version = UptimeKumaVersion()

    async def metrics(self) -> dict[str | int, UptimeKumaMonitor]:
        """Retrieve metrics from Uptime Kuma.

        Fetches and parses Prometheus-style metrics from the Uptime Kuma API endpoint,
        extracting monitor-related metrics and returning them as a dictionary of
        UptimeKumaMonitor objects keyed by monitor name.

        Returns
        -------
        dict[str, UptimeKumaMonitor]
            A dictionary mapping monitor names to their corresponding UptimeKumaMonitor
            objects.

        Raises
        ------
        UptimeKumaAuthenticationException
            If authentication with the Uptime Kuma API fails.
        UptimeKumaConnectionException
            If there is a connection error, timeout, or other client error during the
            request.
        """
        monitors: dict[str | int, dict[str, Any]] = {}
        url = self._base_url / "metrics"

        try:
            request = await self._session.get(
                url, auth=self._auth, timeout=self._timeout
            )
            request.raise_for_status()
        except ClientResponseError as e:
            if e.status is HTTPStatus.UNAUTHORIZED:
                msg = "Authentication failed for %s"
                raise UptimeKumaAuthenticationException(msg, str(url)) from e
            msg = "Request for %s failed with status code %s"
            raise UptimeKumaConnectionException(msg, str(url), e.status) from e
        except TimeoutError as e:
            msg = "Request timeout for %s"
            raise UptimeKumaConnectionException(msg, str(url)) from e
        except ClientError as e:
            raise UptimeKumaConnectionException from e
        else:
            for metric in text_string_to_metric_families(await request.text()):
                if metric.name == "app_version" and metric.samples:
                    self.version = UptimeKumaVersion.from_dict(metric.samples[0].labels)
                if not metric.name.startswith("monitor"):
                    continue
                for sample in metric.samples:
                    key = (
                        int(monitor_id)
                        if (monitor_id := sample.labels.get("monitor_id"))
                        else sample.labels["monitor_name"]
                    )

                    monitors.setdefault(key, sample.labels).update(
                        {sample.name: sample.value}
                    )

            return {
                key: UptimeKumaMonitor.from_dict(value)
                for key, value in monitors.items()
            }
