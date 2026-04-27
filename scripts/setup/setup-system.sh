#!/usr/bin/env bash
# System-level Pi setup: apt packages, I2C, pip packages into conda env.
# Runs on the Pi — called by setup-pi.sh or directly: bash ~/setup-system.sh

set -euo pipefail

CONDA_PIP="$HOME/miniforge3/envs/ros_env/bin/pip"

apt_missing() {
  for pkg in "$@"; do
    dpkg -l "$pkg" 2>/dev/null | grep -q '^ii' || return 0
  done
  return 1
}

APT_PACKAGES=(python3-smbus python3-pip git portaudio19-dev python3-dev i2c-tools libcap-dev)

if apt_missing "${APT_PACKAGES[@]}"; then
  echo "--- Installing apt packages ---"
  sudo apt-get update
  sudo apt-get install -y "${APT_PACKAGES[@]}"
else
  echo "--- apt packages already installed, skipping ---"
fi

echo "--- Enabling I2C ---"
sudo raspi-config nonint do_i2c 0

# Give the conda env access to apt-installed Python packages (libcamera,
# picamera2, etc.) that have no PyPI equivalent.
PTH_FILE="$HOME/miniforge3/envs/ros_env/lib/python3.11/site-packages/system-site-packages.pth"
if [[ ! -f "$PTH_FILE" ]]; then
  echo "--- Adding system site-packages to conda env ---"
  echo "/usr/lib/python3/dist-packages" > "$PTH_FILE"
  echo "/usr/lib/python3.11/dist-packages" >> "$PTH_FILE"
fi

echo "--- Installing pip packages into conda env ---"
"$CONDA_PIP" install -q -r "$HOME/requirements.txt"

echo "--- System setup complete ---"
