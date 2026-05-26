"""Tests for pythonkuma."""

from http import HTTPStatus
from typing import Any
from unittest.mock import AsyncMock, Mock

from aiohttp import ClientError, ClientResponseError, ConnectionTimeoutError
import pytest
from syrupy.assertion import SnapshotAssertion

from pythonkuma import UptimeKuma
from pythonkuma.exceptions import (
    UptimeKumaAuthenticationException,
    UptimeKumaConnectionException,
    UptimeKumaParseException,
)
from pythonkuma.models import MonitorStatus

from .conftest import load_fixture

LIVE_RESPONSE_TIME_MS = 85
PAUSED_UPTIME_RATIO_1D = 0.95
PAUSED_RESPONSE_TIME_SECONDS_1D = 0.42


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
    expected_exception: Exception,
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


async def test_metrics_paused_monitor(mock_session: AsyncMock) -> None:
    """Paused monitors omit ``monitor_status`` and ``monitor_response_time``.

    Uptime Kuma keeps emitting the sliding-window aggregates
    (``monitor_uptime_ratio`` and ``monitor_response_time_seconds``) for paused
    monitors but stops emitting the live ``monitor_status`` and
    ``monitor_response_time`` series. The parser must tolerate this and return
    ``monitor_status = None`` for those monitors instead of crashing the whole
    sync.
    """
    paused_monitor_id = 10
    mock_session.get.return_value.text.return_value = load_fixture("metrics_paused.txt")
    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    response = await uptime_kuma.metrics()

    assert 1 in response
    assert paused_monitor_id in response

    live = response[1]
    assert live.monitor_name == "Home Assistant"
    assert live.monitor_status is MonitorStatus.UP
    assert live.monitor_response_time == LIVE_RESPONSE_TIME_MS

    paused = response[paused_monitor_id]
    assert paused.monitor_name == "Paused Service"
    assert paused.monitor_status is None
    assert paused.monitor_response_time == 0
    assert paused.monitor_uptime_ratio_1d == PAUSED_UPTIME_RATIO_1D
    assert paused.monitor_response_time_seconds_1d == PAUSED_RESPONSE_TIME_SECONDS_1D
