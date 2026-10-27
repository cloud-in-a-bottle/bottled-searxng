import re
import time

import requests
from openhost_test_harness import OpenhostStack


def _get(stack: OpenhostStack, path: str, session: requests.Session, **params: str) -> requests.Response:
    """GET, retrying while the app finishes booting."""
    deadline = time.monotonic() + 60
    while True:
        try:
            response = session.get(f"{stack.url}{path}", params=params, timeout=60)
            if response.status_code < 500 or time.monotonic() > deadline:
                return response
        except requests.ConnectionError:
            if time.monotonic() > deadline:
                raise
        time.sleep(2)


def test_anonymous_visitors_get_the_search_page(stack: OpenhostStack) -> None:
    """public_paths = ["/"] serves SearXNG to anyone, not just the owner."""
    response = _get(stack, "/", requests.Session())
    assert response.status_code == 200 and response.url.startswith(stack.url), (
        f"anonymous GET / ended at {response.url} with {response.status_code}: {response.text[:300]}"
    )


def test_search_page_refuses_framing_and_searches_with_get(stack: OpenhostStack) -> None:
    """Caddy adds anti-framing headers (#6); the seeded settings.yml makes the search form use GET."""
    response = _get(stack, "/", stack.owner_session)
    assert response.headers.get("X-Frame-Options") == "DENY", dict(response.headers)
    assert "frame-ancestors 'none'" in response.headers.get("Content-Security-Policy", ""), dict(response.headers)
    search_forms = [tag for tag in re.findall(r"<form\b[^>]*>", response.text) if 'id="search"' in tag]
    assert search_forms and 'method="GET"' in search_forms[0], f"search form: {search_forms}"


def test_json_and_rss_formats_are_enabled(stack: OpenhostStack) -> None:
    """settings.yml enables the json and rss output formats (#7); upstream's default (html only) answers them with 403."""
    # Results come from external engines, which CI may not reach, so only the response format is checked.
    as_json = _get(stack, "/search", stack.owner_session, q="cloud in a bottle", format="json")
    assert as_json.status_code == 200, f"format=json: {as_json.status_code}: {as_json.text[:300]}"
    assert as_json.json()["query"] == "cloud in a bottle", as_json.text[:300]

    as_rss = _get(stack, "/search", stack.owner_session, q="cloud in a bottle", format="rss")
    assert as_rss.status_code == 200, f"format=rss: {as_rss.status_code}: {as_rss.text[:300]}"
    assert "<rss" in as_rss.text, as_rss.text[:300]


def test_settings_are_stored_in_app_data(stack: OpenhostStack) -> None:
    """start.sh points SearXNG's config at the app data dir, so settings.yml edits survive redeploys and updates."""
    settings = stack.data_dir / "config" / "settings.yml"
    assert settings.exists(), (
        f"{settings} missing; app data dir has {sorted(p.name for p in stack.data_dir.iterdir())}"
    )
