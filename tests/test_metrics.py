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
