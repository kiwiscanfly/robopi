#!/usr/bin/env bash
# Install Python dependencies on the Pi.
# Run this once after first setup, or any time requirements.txt changes.
# Usage: ./scripts/setup-pi.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env file not found. Copy .env.example to .env and configure it."
  exit 1
fi

source "$ENV_FILE"

echo "Installing dependencies on $PI_USER@$PI_HOST..."

echo "Copying requirements.txt to Pi..."
scp "$SCRIPT_DIR/../requirements.txt" "$PI_USER@$PI_HOST:~/requirements.txt"

ssh -t "$PI_USER@$PI_HOST" bash <<'REMOTE'
  set -euo pipefail

  echo "--- Updating apt package lists ---"
  sudo apt-get update

  echo "--- Installing apt packages ---"
  sudo apt-get install -y python3-lgpio python3-gpiozero python3-smbus git portaudio19-dev python3-dev i2c-tools

  echo "--- Enabling I2C ---"
  sudo raspi-config nonint do_i2c 0
  echo "  I2C enabled"

  echo "--- Installing pip dependencies ---"
  VENV_DIR="$HOME/robot-venv"

  if [[ ! -d "$VENV_DIR" ]]; then
    echo "  Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR" --system-site-packages
  fi

  echo "  Installing from requirements.txt..."
  "$VENV_DIR/bin/pip" install -r "$HOME/requirements.txt"

  echo "--- Verifying imports ---"
  "$VENV_DIR/bin/python3" -c "import lgpio; print('  lgpio ok')"
  "$VENV_DIR/bin/python3" -c "import gpiozero; print('  gpiozero ok')"
  "$VENV_DIR/bin/python3" -c "import colorzero; print('  colorzero ok')"
  "$VENV_DIR/bin/python3" -c "from robot_hat import Servo; print('  robot_hat ok')"

  echo "--- I2C device scan ---"
  /usr/sbin/i2cdetect -y 1

  echo "--- Done ---"
REMOTE

echo "Pi is ready."
