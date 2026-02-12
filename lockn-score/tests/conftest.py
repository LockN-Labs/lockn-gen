"""Pytest configuration for LockN Score tests."""

import asyncio
from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def event_loop() -> asyncio.AbstractEventLoop:
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def session_data() -> dict[str, Any]:
    """Return default session data for tests."""
    return {
        "target_rally_count": 100,
        "points_to_win": 11,
        "serve_interval": 5,
        "best_of_sets": 1,
    }