# searxng publishes dated builds only; pin the exact build and its
# multi-arch index digest.
FROM docker.io/searxng/searxng:2026.11.5-3e95f6cd2@sha256:ffad724acd87b8dd312328d18da88ddd42e5c4b1d23231594662620053c13cae

# The SearXNG image is Void Linux-based (no apk/apt). Download a static
# Caddy binary for Host header rewriting (the OpenHost router strips Host
# and sets X-Forwarded-Host; SearXNG needs them to match for correct URLs).
# The checksum is from Caddy's published caddy_2.9.1_checksums.txt. The
# image's busybox sha512sum has no -c, so compare the hash directly.
ARG CADDY_VERSION=2.9.1
ARG CADDY_SHA512=0412057ba591c33bdb66034d7f32209619ce635147dac3084c79abcbc118a761145e695199f57c6798d88fab077f2b0d9cb999f52ded904c6d464a4eba202932
RUN mkdir -p /usr/local/bin && \
    wget -qO /tmp/caddy.tar.gz "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" && \
    test "$(sha512sum /tmp/caddy.tar.gz | cut -d ' ' -f 1)" = "${CADDY_SHA512}" && \
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
