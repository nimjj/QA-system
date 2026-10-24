# Production Dockerfile for QA Analysis System
# ---- build stage: needs git for pinned Laya install ----
FROM python:3.14-slim AS build
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /build
# CPU-only torch
RUN pip install --no-cache-dir torch==2.14.1 --index-url https://download.pytorch.org/whl/cpu
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# ---- final production stage: unprivileged user, no build tools ----
FROM python:3.14-slim
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LAYA_FLOW=v3 \
    LAYA_CHECKPOINT="" \
    HF_HOME=/tmp/hf_home

RUN useradd --create-home --uid 1000 qa
WORKDIR /app
COPY main.py ./
COPY src/ src/
COPY resources/ resources/
COPY inputs/ inputs/
COPY Scripts/ Scripts/
RUN mkdir -p logs models && chown -R qa:qa /app
USER qa

EXPOSE 8006
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8006/ready', timeout=4).status == 200 else 1)"

CMD ["uvicorn", "src.api.web_app:app", "--host", "0.0.0.0", "--port", "8006"]
