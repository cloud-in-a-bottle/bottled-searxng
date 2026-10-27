# searxng publishes dated builds only; pin the exact build and its
# multi-arch index digest.
FROM docker.io/searxng/searxng:2026.10.27-ef7bae9dd@sha256:64936ab0847aae6494d37edf688ce792b262e8467d48ad844c0bf3f899a45249

# The SearXNG image is Void Linux-based (no apk/apt). Download a static
# Caddy binary for Host header rewriting (the OpenHost router strips Host
# and sets X-Forwarded-Host; SearXNG needs them to match for correct URLs).
# The checksum is from Caddy's published caddy_2.9.1_checksums.txt.
ARG CADDY_VERSION=2.9.1
ARG CADDY_SHA512=0412057ba591c33bdb66034d7f32209619ce635147dac3084c79abcbc118a761145e695199f57c6798d88fab077f2b0d9cb999f52ded904c6d464a4eba202932
RUN mkdir -p /usr/local/bin && \
    wget -qO /tmp/caddy.tar.gz "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" && \
    echo "${CADDY_SHA512}  /tmp/caddy.tar.gz" | sha512sum -c - && \
    tar -xzf /tmp/caddy.tar.gz -C /usr/local/bin caddy && \
    chmod +x /usr/local/bin/caddy && \
    rm /tmp/caddy.tar.gz

# Copy our startup wrapper and Caddyfile
COPY start.sh /app/start.sh
COPY Caddyfile /app/Caddyfile
RUN chmod +x /app/start.sh

EXPOSE 3000

ENTRYPOINT []
CMD ["/app/start.sh"]
