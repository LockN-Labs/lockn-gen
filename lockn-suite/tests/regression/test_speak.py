import os

import pytest


PROFILE_ID = os.getenv("LOCKN_SPEAK_PROFILE_ID", "11111111-1111-1111-1111-111111111111")


def _synthesize(client, base_url: str, text: str, fmt: str = "wav"):
    return client.post(
        f"{base_url}/api/tts/",
        json={"text": text, "profileId": PROFILE_ID, "format": fmt},
    )


@pytest.mark.regression
@pytest.mark.smoke
def test_speak_health(client, base_urls):
    res = client.get(f"{base_urls['speak']}/health")
    assert res.status_code == 200


@pytest.mark.regression
def test_speak_profiles_list(client, base_urls):
    res = client.get(f"{base_urls['speak']}/api/profiles/")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: TTS backend intermittently down returning 502 (Linear ticket pending)",
    strict=False,
)
def test_speak_tts_wav(client, base_urls):
    """Known gap: synthesis endpoint currently fails due to TTS backend 502."""
    res = _synthesize(client, base_urls["speak"], "Regression WAV synthesis", "wav")
    assert res.status_code == 200
    assert "audio/wav" in res.headers.get("content-type", "")


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: TTS backend intermittently down returning 502 (Linear ticket pending)",
    strict=False,
)
def test_speak_tts_mp3(client, base_urls):
    """Known gap: synthesis endpoint currently fails due to TTS backend 502."""
    res = _synthesize(client, base_urls["speak"], "Regression MP3 synthesis", "mp3")
    assert res.status_code == 200
    assert "audio/mpeg" in res.headers.get("content-type", "")
