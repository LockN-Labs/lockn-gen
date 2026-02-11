import json
import socket
import uuid
from datetime import datetime, timezone

import pytest


def _iso_now():
    return datetime.now(timezone.utc).isoformat()


@pytest.fixture(scope="module")
def seeded_receipt(client, base_urls):
    unique = uuid.uuid4().hex[:12]
    source = f"qa-regression-{unique}"
    tag = f"tag-{unique}"

    payload = {
        "model": "qa-model",
        "provider": "qa-provider",
        "sessionId": f"qa-session-{unique}",
        "timestamp": _iso_now(),
        "usage": {"input": 123, "output": 45},
        "cost": {"total": 0.0123},
    }

    resp = client.post(
        f"{base_urls['logger_api']}/api/receipts/",
        json={"source": source, "payloadJson": json.dumps(payload), "tags": ["qa", tag]},
    )
    assert resp.status_code in (200, 201), f"Ingestion failed: {resp.status_code} {resp.text}"

    return {"id": resp.json().get("id"), "source": source, "tag": tag}


@pytest.mark.regression
@pytest.mark.smoke
def test_logger_health(client, base_urls):
    r = client.get(f"{base_urls['logger_api']}/health")
    assert r.status_code == 200


@pytest.mark.regression
def test_logger_ingest_and_retrieve(client, base_urls, seeded_receipt):
    r = client.get(f"{base_urls['logger_api']}/api/receipts/{seeded_receipt['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == seeded_receipt["id"]


@pytest.mark.regression
def test_logger_search_filter(client, base_urls, seeded_receipt):
    by_source = client.get(
        f"{base_urls['logger_api']}/api/receipts/",
        params={"source": seeded_receipt["source"], "pageSize": 10},
    )
    assert by_source.status_code == 200


@pytest.mark.regression
def test_logger_storage_backend_health(client, base_urls):
    r = client.get(f"{base_urls['seaweed']}/healthz")
    assert r.status_code == 200


@pytest.mark.regression
def test_logger_redis_connectivity(base_urls):
    with socket.create_connection((base_urls["redis_host"], base_urls["redis_port"]), timeout=3) as sock:
        sock.sendall(b"*1\r\n$4\r\nPING\r\n")
        data = sock.recv(64)
    assert data.startswith(b"+PONG")
