#!/usr/bin/env bash
# Copy a file to the Pi and run it
# Usage: ./scripts/deploy-run.sh path/to/file.py

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env file not found. Copy .env.example to .env and configure it."
  exit 1
fi

source "$ENV_FILE"

FILE="${1:-}"
if [[ -z "$FILE" ]]; then
  echo "Usage: $0 <file>"
  exit 1
fi

if [[ ! -f "$FILE" ]]; then
  echo "Error: file not found: $FILE"
  exit 1
fi

RELATIVE_PATH="${FILE#./}"
REMOTE_PATH="$PI_DEPLOY_DIR/$RELATIVE_PATH"
REMOTE_DIR="$(dirname "$REMOTE_PATH")"

echo "Deploying $FILE to $PI_USER@$PI_HOST:$REMOTE_PATH"
ssh "$PI_USER@$PI_HOST" "mkdir -p $REMOTE_DIR"
scp "$FILE" "$PI_USER@$PI_HOST:$REMOTE_PATH"

echo "Running $REMOTE_PATH on $PI_HOST..."
ssh -t "$PI_USER@$PI_HOST" "~/robot-venv/bin/python3 $REMOTE_PATH"
