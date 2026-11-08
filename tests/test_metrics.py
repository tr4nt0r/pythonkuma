"""Tests for pythonkuma."""

from collections.abc import Iterable
from http import HTTPStatus
import threading
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

from aiohttp import ClientError, ClientResponseError, ConnectionTimeoutError
from prometheus_client.metrics_core import Metric
from prometheus_client.parser import text_string_to_metric_families
import pytest
from syrupy.assertion import SnapshotAssertion

from pythonkuma import UptimeKuma
from pythonkuma.exceptions import (
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaParseException,
)


async def test_metrics(mock_session: AsyncMock, snapshot: SnapshotAssertion) -> None:
    """Test metrics."""
    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    response = await uptime_kuma.metrics()

    assert {k: v.to_dict() for k, v in response.items()} == snapshot

    assert uptime_kuma.version.version == "2.1.0"
    assert uptime_kuma.version.major == "2"
    assert uptime_kuma.version.minor == "1"
    assert uptime_kuma.version.patch == "0"


@pytest.mark.parametrize(
    ("exception", "expected_exception", "error_msg"),
    [
        (
            ClientResponseError(
                request_info=Mock(), history=(Mock()), status=HTTPStatus.NOT_FOUND
            ),
            UptimeKumaConnectionException,
            (
                "Request for %s failed with status code %s",
                "http://uptime.example.com/metrics",
                HTTPStatus.NOT_FOUND,
            ),
        ),
        (
            ClientResponseError(
                request_info=Mock(), history=(Mock()), status=HTTPStatus.UNAUTHORIZED
            ),
            UptimeKumaAuthenticationException,
            ("Authentication failed for %s", "http://uptime.example.com/metrics"),
        ),
        (ClientError, UptimeKumaConnectionException, ()),
        (
            ConnectionTimeoutError,
            UptimeKumaConnectionException,
            ("Request timeout for %s", "http://uptime.example.com/metrics"),
        ),
    ],
)
async def test_exceptions(
    mock_session: AsyncMock,
    exception: Exception,
    expected_exception: type[Exception],
    error_msg: tuple[Any],
) -> None:
    """Test request exceptions."""
    mock_session.get.side_effect = exception
    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    with pytest.raises(expected_exception) as e:
        await uptime_kuma.metrics()

    assert e.value.args == error_msg


async def test_metrics_parse_exceptions(mock_session: AsyncMock) -> None:
    """Test prometheus metrics parsing fails."""
    mock_session.get.return_value.text.return_value = "invalid metrics"
    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    with pytest.raises(UptimeKumaParseException):
        await uptime_kuma.metrics()


async def test_metrics_parsed_off_event_loop(mock_session: AsyncMock) -> None:
    """Test prometheus metrics are parsed in a worker thread, not the event loop."""
    loop_thread = threading.get_ident()
    parse_threads: list[int] = []

    def recording_parser(text: str) -> Iterable[Metric]:
        parse_threads.append(threading.get_ident())
        return text_string_to_metric_families(text)

    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    with patch(
        "pythonkuma.uptimekuma.text_string_to_metric_families", recording_parser
    ):
        monitors = await uptime_kuma.metrics()

    assert monitors
    assert parse_threads
    assert loop_thread not in parse_threads
