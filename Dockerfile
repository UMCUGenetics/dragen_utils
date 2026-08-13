FROM ghcr.io/astral-sh/uv:0.12.3-python3.14-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Dependencies first, so this layer caches independently of source changes.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# README.md is required by the build backend -- pyproject sets `readme = "README.md"`.
COPY README.md ./
COPY src ./src
# --no-editable copies the package into the venv instead of linking back to /app/src, so the
# runtime stage below only needs the venv.
RUN uv sync --frozen --no-dev --no-editable


FROM python:3.14-slim-trixie

# Nextflow's .command.run polls `ps` to collect per-task CPU and memory metrics; the slim base
# image does not ship it. Installed before the venv copy so this layer caches across code changes.
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["dragen-utils", "--help"]