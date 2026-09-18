#!/usr/bin/env bash
set -e

MODELS_DIR="/app/models"
mkdir -p "$MODELS_DIR"

# Skip heavy model downloads in container/demo environments unless explicitly requested.
if [ "${SKIP_MODEL_DOWNLOAD:-false}" != "true" ]; then
  # Download Gemma 3 4B Q4_K_M if missing
  GEMMA_FILE="$MODELS_DIR/gemma-3-4b-it-Q4_K_M.gguf"
  GEMMA_REPO_FILE="google_gemma-3-4b-it-Q4_K_M.gguf"
  if [ ! -f "$GEMMA_FILE" ]; then
      echo "=========================================="
      echo "Downloading Gemma 3 4B Q4_K_M (~2.5GB)..."
      echo "This is a one-time download."
      echo "=========================================="
      huggingface-cli download \
          bartowski/google_gemma-3-4b-it-GGUF \
          --include "$GEMMA_REPO_FILE" \
          --local-dir "$MODELS_DIR" \
          --local-dir-use-symlinks False
      # Create symlink to the expected name
      if [ -f "$MODELS_DIR/$GEMMA_REPO_FILE" ]; then
          ln -s "$MODELS_DIR/$GEMMA_REPO_FILE" "$GEMMA_FILE"
      fi
      echo "Gemma 3 download complete."
  else
      echo "Gemma 3 model already present."
  fi

  # Download Whisper tiny if missing
  WHISPER_FILE="$MODELS_DIR/ggml-tiny.bin"
  if [ ! -f "$WHISPER_FILE" ]; then
      echo "=========================================="
      echo "Downloading Whisper tiny (~39MB)..."
      echo "This is a one-time download."
      echo "=========================================="
      wget -q --show-progress \
          -O "$WHISPER_FILE" \
          "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-tiny.bin"
      echo "Whisper tiny download complete."
  else
      echo "Whisper tiny already present."
  fi
else
  echo "SKIP_MODEL_DOWNLOAD is set; skipping model downloads."
fi

# Start uvicorn
echo "Starting Mirage backend..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-config ./uvicorn_log_config.json
