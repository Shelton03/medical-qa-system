# Stage 1: Install dependencies (including build tools for llama-cpp)
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime image with hot-reload support
FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/models \
    && chown -R appuser:appuser /app

# Install runtime deps + wget/ffmpeg for model download + whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    git \
    libopenblas0 \
    libgomp1 \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=builder /usr/local/bin/alembic /usr/local/bin/alembic
COPY --from=builder /usr/local/bin/pytest /usr/local/bin/pytest
COPY --from=builder /usr/local/bin/huggingface-cli /usr/local/bin/huggingface-cli

COPY main.py ./
COPY app ./app
COPY start_backend.sh ./
RUN chmod +x start_backend.sh

RUN chown -R appuser:appuser /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

CMD ["./start_backend.sh"]
