import re
from urllib.parse import urljoin

import pytest


@pytest.mark.regression
@pytest.mark.smoke
def test_platform_health_endpoints(client, base_urls):
    r_web = client.get(f"{base_urls['platform_web']}/health")
    r_api = client.get(f"{base_urls['platform_api']}/health")
    r_upstream = client.get(f"{base_urls['platform_upstream']}/health")

    assert r_web.status_code == 200
    assert r_api.status_code == 200
    assert r_upstream.status_code == 200


@pytest.mark.regression
def test_platform_landing_routes(client, base_urls):
    routes = ["/", "/score/", "/speak/", "/gen/", "/waitlist/"]
    bad = []
    for path in routes:
        r = client.get(f"{base_urls['platform_web']}{path}")
        if r.status_code != 200:
            bad.append((path, r.status_code))
    assert not bad, f"Non-200 routes: {bad}"


@pytest.mark.regression
@pytest.mark.known_failure
@pytest.mark.xfail(
    reason="Known gap: waitlist POST not implemented (LOC-421)",
    strict=False,
)
def test_platform_waitlist_post(client, base_urls):
    """Known gap tracked in Linear: LOC-421."""
    payload = {"email": "qa+waitlist@example.com", "name": "QA Bot"}
    r = client.post(f"{base_urls['platform_web']}/waitlist", json=payload)
    assert r.status_code in {200, 201, 202, 204}


@pytest.mark.regression
def test_platform_static_asset_serving(client, base_urls):
    page = client.get(f"{base_urls['platform_web']}/score/")
    assert page.status_code == 200

    matches = re.findall(r'src=["\']([^"\']+\.js)["\']', page.text)
    assert matches, "No JS assets found in /score/ HTML"

    asset_url = urljoin(f"{base_urls['platform_web']}/score/", matches[0])
    asset = client.get(asset_url)
    assert asset.status_code == 200
    assert len(asset.content) > 0
