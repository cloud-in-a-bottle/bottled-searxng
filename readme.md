# bottled-searxng

[SearXNG](https://github.com/searxng/searxng) is a privacy-respecting metasearch
engine that aggregates results from many other search engines without tracking
you. This repository packages it as a Cloud in a Bottle app.

## What you get

- SearXNG running on `https://searxng.<zone>/`.
- Public: anyone with the URL can search. No SSO.
- Results gathered from many engines behind one search box.
- Image results proxied through your instance, so the sites hosting them never see who is searching.
- No external database. Configuration and cache live in the app's storage.

## Usage

Open `https://searxng.<zone>/` and search. Open Preferences to choose engines,
categories, theme, and safe-search level. Searches use GET requests, so you can
bookmark and share result-page links.

## Data

Persistent data lives under `$OPENHOST_APP_DATA_DIR/`:

- `config/settings.yml`: SearXNG configuration
- `data/`: cached data such as favicons

To change engines or other settings, edit `config/settings.yml` in the app's
data directory and restart the app.

## Resources

About 512 MB RAM and 0.25 CPU cores. The container image is roughly 180 MB.

## License

SearXNG is licensed under the GNU Affero General Public License v3.0 or later
(AGPL-3.0-or-later). Because the image built from this repository includes
SearXNG, the image as a whole is distributed under the AGPL-3.0; see `LICENSE`.
The corresponding source is upstream `searxng/searxng`; attribution, the source
offer, and third-party component notices (Caddy, Apache-2.0) are in `NOTICE`.

The packaging files original to this repository (`Dockerfile`, `Caddyfile`,
`start.sh`, `openhost.toml`, and docs) are additionally offered under the MIT
License (see `NOTICE`).
