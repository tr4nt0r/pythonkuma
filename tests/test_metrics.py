"""Tests for pythonkuma."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from pythonkuma import UptimeKuma


async def test_metrics(mock_session: AsyncMock, snapshot: SnapshotAssertion) -> None:
    """Test metrics."""
    uptime_kuma = UptimeKuma(mock_session, "http://uptime.example.com", "test-apikey")

    response = await uptime_kuma.metrics()

    assert {k: v.to_dict() for k, v in response.items()} == snapshot
