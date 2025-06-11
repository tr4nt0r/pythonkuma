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
from .models import UptimeKumaMonitor


class UptimeKuma:
    """Uptime Kuma client."""

    def __init__(
        self,
        session: ClientSession,
        base_url: URL | str,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Initialize the Uptime Kuma client."""
        self._base_url = base_url if isinstance(base_url, URL) else URL(base_url)

        self._auth = BasicAuth("", api_key) if api_key else None

        self._timeout = ClientTimeout(total=timeout or 10)
        self._session = session

    async def metrics(self) -> list[UptimeKumaMonitor]:
        """Retrieve metrics from Uptime Kuma."""
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
            parsed = text_string_to_metric_families(await request.text())

            monitors: dict[str, dict[str, Any]] = {}
            for metric in parsed:
                if not metric.name.startswith("monitor"):
                    continue
                for sample in metric.samples:
                    if not (monitor_name := sample.labels.get("monitor_name")):
                        continue

                    monitors.setdefault(monitor_name, sample.labels).update(
                        {sample.name: sample.value}
                    )

            return {
                key: UptimeKumaMonitor.from_dict(value)
                for key, value in monitors.items()
            }
