import io
import math
import struct
import wave

import pytest


def make_wav_bytes(duration_s: float = 1.0, sr: int = 16000, freq: float = 440.0) -> bytes:
    n = int(duration_s * sr)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        frames = bytearray()
        for i in range(n):
            sample = int(0.2 * 32767 * math.sin(2 * math.pi * freq * (i / sr)))
            frames += struct.pack("<h", sample)
        wf.writeframes(bytes(frames))
    return buf.getvalue()


@pytest.fixture(scope="module")
def wav_bytes():
    return make_wav_bytes()


@pytest.mark.regression
@pytest.mark.smoke
def test_listen_brain_service_health(client, base_urls):
    for key in ("panns", "brain"):
        r = client.get(f"{base_urls[key]}/health")
        assert r.status_code == 200, f"{key} health failed: {r.status_code} {r.text[:200]}"


@pytest.mark.regression
def test_panns_classification(client, base_urls, wav_bytes):
    files = {"file": ("sample.wav", wav_bytes, "audio/wav")}
    r = client.post(f"{base_urls['panns']}/v1/audio/classify", files=files, data={"top_k": "5"})
    assert r.status_code == 200
    payload = r.json()
    assert "tags" in payload and isinstance(payload["tags"], list)


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: chatterbox port mismatch and whisper healthcheck route is incorrect (Linear tickets pending)",
    strict=False,
)
def test_whisper_and_chatterbox_health(client, base_urls):
    """Known stack gap: whisper and chatterbox are not aligned with expected network/health config."""
    whisper = client.get(f"{base_urls['whisper']}/health")
    chatterbox = client.get(f"{base_urls['chatterbox']}/health")
    assert whisper.status_code == 200
    assert chatterbox.status_code == 200


@pytest.mark.regression
def test_brain_openapi_routes(client, base_urls):
    openapi = client.get(f"{base_urls['brain']}/openapi.json")
    assert openapi.status_code == 200
    paths = set(openapi.json().get("paths", {}).keys())
    assert "/chat" in paths
    assert "/tts/synthesize" in paths
