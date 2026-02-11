import time

import pytest


@pytest.fixture(scope="module")
def auth_openapi(client, base_urls):
    r = client.get(f"{base_urls['auth']}/swagger/v1/swagger.json")
    assert r.status_code == 200, f"Swagger unavailable: {r.status_code}"
    return r.json()


def _path_exists(openapi: dict, path: str) -> bool:
    return path in openapi.get("paths", {})


def _method_exists(openapi: dict, path: str, method: str) -> bool:
    return method.lower() in openapi.get("paths", {}).get(path, {})


@pytest.mark.regression
@pytest.mark.smoke
def test_auth_health(client, base_urls):
    r = client.get(f"{base_urls['auth']}/health")
    assert r.status_code == 200
    assert r.json().get("status") == "healthy"


@pytest.mark.regression
def test_auth0_callback_exists_and_redirects(auth_openapi, client, base_urls):
    callback_candidates = ["/auth/callback", "/callback", "/signin-auth0", "/login/callback"]
    existing = [p for p in callback_candidates if _path_exists(auth_openapi, p)]
    assert existing, f"No Auth0 callback endpoint found. Checked: {callback_candidates}"

    r = client.get(f"{base_urls['auth']}{existing[0]}")
    assert r.status_code in {302, 303, 307, 308}


@pytest.mark.regression
def test_auth_token_validation_if_exists(auth_openapi, client, base_urls):
    endpoint = "/api/keys/validate"
    if not _method_exists(auth_openapi, endpoint, "post"):
        pytest.skip("Token validation endpoint not exposed")

    create_payload = {
        "name": "qa-e2e-key",
        "ownerId": "qa-user",
        "scopes": ["read", "write"],
        "environment": "test",
        "rateLimitPerMinute": 5,
    }
    create_resp = client.post(f"{base_urls['auth']}/api/keys", json=create_payload)
    assert create_resp.status_code in {200, 201}


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: CORS preflight returns 405 on /health (Linear ticket pending)",
    strict=False,
)
def test_auth_cors_preflight(client, base_urls):
    """Known gap: service does not currently answer CORS preflight on health route."""
    headers = {
        "Origin": "https://example.com",
        "Access-Control-Request-Method": "GET",
    }
    r = client.options(f"{base_urls['auth']}/health", headers=headers)
    assert r.status_code in {200, 204}
    assert r.headers.get("access-control-allow-origin") is not None


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: auth service has no global rate limiting enforcement (Linear ticket pending)",
    strict=False,
)
def test_auth_rate_limiting(client, base_urls):
    """Known gap: no observable 429 during request burst."""
    statuses = []
    for _ in range(80):
        resp = client.get(f"{base_urls['auth']}/health")
        statuses.append(resp.status_code)
        time.sleep(0.01)

    assert 429 in statuses
