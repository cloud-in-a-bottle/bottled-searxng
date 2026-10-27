import time

from openhost_test_harness import OpenhostStack


def test_app_serves_owner(stack: OpenhostStack) -> None:
    # The app is marked running once its health check passes; "/" can take a little longer to come up.
    deadline = time.monotonic() + 60
    while True:
        response = stack.owner_session.get(f"{stack.url}/", timeout=30)
        if response.status_code < 400 or time.monotonic() > deadline:
            break
        time.sleep(2)
    assert response.status_code < 400, (
        f"GET / returned {response.status_code}: {response.text[:500]}\n\napp logs:\n{stack.app_logs()[-5000:]}"
    )


def test_base_url_matches_router_url(stack: OpenhostStack) -> None:
    # SearXNG builds absolute links (here, the OpenSearch search template) from its base_url, which start.sh
    # derives from OPENHOST_ZONE_DOMAIN. The harness zone is "harness.localhost:<port>", so base_url must be
    # plain http with that port, exactly as the router serves the app.
    response = stack.owner_session.get(f"{stack.url}/opensearch.xml", timeout=30)
    assert response.status_code == 200, f"GET /opensearch.xml returned {response.status_code}: {response.text[:500]}"
    assert f'template="{stack.url}/search' in response.text, response.text[:2000]
