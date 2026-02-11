"""Fixtures for pythonkuma."""

from collections.abc import Generator
from functools import lru_cache
import pathlib
from unittest.mock import AsyncMock

from aiohttp import ClientResponse
import pytest


@lru_cache
def load_fixture(filename: str) -> str:
    """Load a fixture."""
    return (
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf-8")
    )


@pytest.fixture
def mock_session() -> Generator[AsyncMock]:
    """Mock aiohttp ClientSession."""
    mock_session = AsyncMock()
    mock_response = AsyncMock(spec=ClientResponse, status=200)
    mock_response.text.return_value = load_fixture("metrics.txt")

    mock_session.get.return_value = mock_response

    return mock_session
