import asyncio
import json
import uuid

import httpx
import pytest
import websockets


async def _create_session(client: httpx.AsyncClient, mode: str = "game") -> str:
    r = await client.post(f"/api/session/{mode}", json={})
    assert r.status_code == 200, f"create {mode} failed: {r.status_code} {r.text}"
    data = r.json()
    assert "session_id" in data
    return data["session_id"]


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.asyncio
async def test_score_session_crud(async_score_client):
    session_id = await _create_session(async_score_client, mode="game")

    get_resp = await async_score_client.get(f"/api/session/{session_id}")
    assert get_resp.status_code == 200, get_resp.text

    delete_resp = await async_score_client.delete(f"/api/session/{session_id}")
    assert delete_resp.status_code == 200, delete_resp.text


@pytest.mark.regression
@pytest.mark.asyncio
async def test_score_websocket_handshake(score_ws_url):
    room = f"regression-{uuid.uuid4().hex[:8]}"
    uri = f"{score_ws_url}/ws/{room}"

    async with websockets.connect(uri) as ws:
        raw = await asyncio.wait_for(ws.recv(), timeout=5)
        msg = json.loads(raw)
        assert msg.get("type") == "welcome"
        assert msg.get("room") == room


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: missing player join endpoint (Linear ticket pending)",
    strict=False,
)
@pytest.mark.asyncio
async def test_score_player_join_endpoint_exists(async_score_client):
    """Known gap: no player-join endpoint is currently exposed in Score API."""
    session_id = await _create_session(async_score_client, mode="game")

    candidate_paths = [
        f"/api/session/{session_id}/join",
        f"/api/session/{session_id}/players/join",
        f"/api/session/{session_id}/player/join",
    ]

    for path in candidate_paths:
        resp = await async_score_client.post(path, json={"player": "qa-player"})
        if resp.status_code != 404:
            return

    pytest.fail("No player join endpoint found in known candidate routes")
