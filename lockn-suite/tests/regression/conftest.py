import os

import httpx
import pytest
import pytest_asyncio


@pytest.fixture(scope="session")
def base_urls():
    """Centralized service URLs for the LockN stack."""
    return {
        "score_http": os.getenv("SCORE_BASE_URL", "http://localhost:8000").rstrip("/"),
        "score_ws": os.getenv("SCORE_WS_URL", "").rstrip("/"),
        "auth": os.getenv("AUTH_BASE_URL", "http://localhost:5200").rstrip("/"),
        "platform_web": os.getenv("PLATFORM_WEB_BASE_URL", "http://localhost:3080").rstrip("/"),
        "platform_api": os.getenv("PLATFORM_API_BASE_URL", "http://localhost:3080/score-api").rstrip("/"),
        "platform_upstream": os.getenv("PLATFORM_UPSTREAM_API_BASE_URL", "http://localhost:3181").rstrip("/"),
        "speak": os.getenv("LOCKN_SPEAK_BASE_URL", "http://localhost:3003").rstrip("/"),
        "speak_test_env": os.getenv("LOCKN_SPEAK_TEST_ENV_URL", "http://localhost:3103").rstrip("/"),
        "logger_api": os.getenv("LOGGER_API_BASE_URL", "http://localhost:8080").rstrip("/"),
        "seaweed": os.getenv("SEAWEED_BASE_URL", "http://localhost:8888").rstrip("/"),
        "redis_host": os.getenv("REDIS_HOST", "localhost"),
        "redis_port": int(os.getenv("REDIS_PORT", "6379")),
        "whisper": os.getenv("WHISPER_BASE_URL", "http://127.0.0.1:8890").rstrip("/"),
        "panns": os.getenv("PANNS_BASE_URL", "http://127.0.0.1:8893").rstrip("/"),
        "chatterbox": os.getenv("CHATTERBOX_BASE_URL", "http://127.0.0.1:8084").rstrip("/"),
        "brain": os.getenv("BRAIN_BASE_URL", "http://127.0.0.1:8100").rstrip("/"),
    }


@pytest.fixture(scope="session")
def http_timeout():
    return httpx.Timeout(20.0, connect=5.0)


@pytest.fixture(scope="session")
def client(http_timeout):
    with httpx.Client(timeout=http_timeout, follow_redirects=True) as c:
        yield c


@pytest_asyncio.fixture
async def async_score_client(base_urls):
    timeout = httpx.Timeout(20.0)
    async with httpx.AsyncClient(base_url=base_urls["score_http"], timeout=timeout) as c:
        yield c


@pytest.fixture(scope="session")
def score_ws_url(base_urls):
    ws = base_urls["score_ws"]
    if ws:
        return ws

    base = base_urls["score_http"]
    if base.startswith("https://"):
        return "wss://" + base[len("https://"):]
    if base.startswith("http://"):
        return "ws://" + base[len("http://"):]
    return base
