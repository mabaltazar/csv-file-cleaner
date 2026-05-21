# ── Stage 1: base image with uv installed ─────────────────────────────────────
FROM python:3.12-slim

# Install uv from the official image (fast, no pip needed)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages without activating it
ENV PATH="/app/.venv/bin:$PATH"

# ── Stage 2: install dependencies ─────────────────────────────────────────────
# Copy lockfile and project manifest first (maximizes Docker layer caching)
# If these files don't change, Docker skips this step on rebuild
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# Install dependencies into the container's system Python (no venv needed in Docker)
# --frozen ensures uv.lock is respected exactly — no silent version changes
RUN uv sync --frozen --no-dev

# ── Stage 3: copy source code ──────────────────────────────────────────────────
COPY cleaner.py test_cleaner.py ./

# Default command: run the test suite
CMD ["uv","run","pytest", "test_cleaner.py", "-v"]