# LockN Regression Test Suite

Consolidated permanent regression coverage from the stack-wide QA sweep.

## Layout

- `tests/regression/test_score.py`
- `tests/regression/test_auth.py`
- `tests/regression/test_platform.py`
- `tests/regression/test_speak.py`
- `tests/regression/test_logger.py`
- `tests/regression/test_listen_brain.py`
- `tests/regression/conftest.py` (shared fixtures/base URLs/http clients)

## Markers

- `@pytest.mark.smoke` → critical health checks
- `@pytest.mark.regression` → full suite membership
- `@pytest.mark.known_failure` → known gaps documented as `xfail`

## Run tests

From `lockn-suite/`:

### Smoke only

```bash
pytest -m smoke -q
```

### Full regression

```bash
pytest -m regression -q
```

### Exclude known failures

```bash
pytest -m "regression and not known_failure" -q
```

## Environment overrides

All service URLs can be overridden via environment variables in `conftest.py`, e.g.:

- `SCORE_BASE_URL`
- `AUTH_BASE_URL`
- `PLATFORM_WEB_BASE_URL`
- `PLATFORM_API_BASE_URL`
- `LOCKN_SPEAK_BASE_URL`
- `LOGGER_API_BASE_URL`
- `WHISPER_BASE_URL`, `PANNS_BASE_URL`, `CHATTERBOX_BASE_URL`, `BRAIN_BASE_URL`

## Known failures encoded in suite

- Score: missing player join endpoint
- Auth: CORS preflight 405, no rate limiting
- Platform: no waitlist POST (`LOC-421`)
- Speak: TTS backend returns 502
- Listen/Brain: Chatterbox port mismatch, Whisper healthcheck mismatch
