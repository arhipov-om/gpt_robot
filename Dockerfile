FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /build
COPY pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv lock && \
    uv sync --no-dev

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src"

RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY --from=builder /build/.venv /opt/venv

COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser main.py .

USER appuser

CMD ["python", "main.py"]