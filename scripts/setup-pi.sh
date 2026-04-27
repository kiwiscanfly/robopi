#!/usr/bin/env bash
# Orchestrate full Pi setup: sync files then run each setup script in order.
# Safe to re-run — each sub-script skips steps that are already complete.
# Usage: ./scripts/setup-pi.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env file not found. Copy .env.example to .env and configure it."
  exit 1
fi

source "$ENV_FILE"

echo "=== PiDog setup: $PI_USER@$PI_HOST ==="

echo "--- Copying SSH key ---"
ssh-copy-id "$PI_USER@$PI_HOST"

echo "--- Syncing files to Pi ---"
scp "$SCRIPT_DIR/../requirements.txt"           "$PI_USER@$PI_HOST:~/requirements.txt"
scp "$SCRIPT_DIR/setup/setup-system.sh"     "$PI_USER@$PI_HOST:~/setup-system.sh"
scp "$SCRIPT_DIR/setup/setup-sunfounder.sh" "$PI_USER@$PI_HOST:~/setup-sunfounder.sh"
scp "$SCRIPT_DIR/setup/setup-service.sh"    "$PI_USER@$PI_HOST:~/setup-service.sh"
scp "$SCRIPT_DIR/setup/start-pidog.sh"     "$PI_USER@$PI_HOST:~/start-pidog.sh"
scp "$SCRIPT_DIR/setup/pidog.service"      "$PI_USER@$PI_HOST:~/pidog.service"
scp "$SCRIPT_DIR/setup/verify.sh"           "$PI_USER@$PI_HOST:~/verify.sh"
scp "$SCRIPT_DIR/setup/install-ros2.sh"     "$PI_USER@$PI_HOST:~/install-ros2.sh"
scp "$SCRIPT_DIR/setup/setup-workspace.sh"  "$PI_USER@$PI_HOST:~/setup-workspace.sh"
chmod +x "$SCRIPT_DIR"/setup/*.sh

rsync -a --delete "$SCRIPT_DIR/../pidog_ros2/" "$PI_USER@$PI_HOST:~/pidog_ros2/"
rsync -a --delete "$SCRIPT_DIR/../webui/"      "$PI_USER@$PI_HOST:~/pidog_webui/"

echo "--- Running setup scripts on Pi ---"
ssh -t "$PI_USER@$PI_HOST" bash <<'REMOTE'
  set -euo pipefail
  bash ~/setup-system.sh
  bash ~/install-ros2.sh
  bash ~/setup-sunfounder.sh
  bash ~/setup-workspace.sh
  bash ~/setup-service.sh
  bash ~/verify.sh
  echo "=== Done ==="
REMOTE

echo "Pi is ready."
