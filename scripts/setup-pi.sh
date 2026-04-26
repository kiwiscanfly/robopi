#!/usr/bin/env bash
# Install Python dependencies and ROS 2 on the Pi.
# Safe to re-run — skips steps that are already complete.
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

echo "Copying SSH key to Pi (you'll be prompted for your password once)..."
ssh-copy-id "$PI_USER@$PI_HOST"

echo "Copying files to Pi..."
scp "$SCRIPT_DIR/../requirements.txt" "$PI_USER@$PI_HOST:~/requirements.txt"
scp "$SCRIPT_DIR/../03-ros2/install-ros2.sh" "$PI_USER@$PI_HOST:~/install-ros2.sh"
scp "$SCRIPT_DIR/../03-ros2/setup-workspace.sh" "$PI_USER@$PI_HOST:~/setup-workspace.sh"
chmod +x "$SCRIPT_DIR/../03-ros2/install-ros2.sh" "$SCRIPT_DIR/../03-ros2/setup-workspace.sh"

echo "Syncing pidog_ros2 package to Pi..."
rsync -a --delete "$SCRIPT_DIR/../pidog_ros2/" "$PI_USER@$PI_HOST:~/pidog_ros2/"

ssh -t "$PI_USER@$PI_HOST" bash <<'REMOTE'
  set -euo pipefail

  CONDA_PYTHON="$HOME/miniforge3/envs/ros_env/bin/python3"
  CONDA_PIP="$HOME/miniforge3/envs/ros_env/bin/pip"

  # Returns true if any of the given apt packages are not installed
  apt_missing() {
    for pkg in "$@"; do
      dpkg -l "$pkg" 2>/dev/null | grep -q '^ii' || return 0
    done
    return 1
  }

  # Clones or pulls a git repo. Returns 0 if changes were fetched, 1 if already up to date.
  git_sync() {
    local url="$1" dir="$2"; shift 2
    if [[ -d "$dir" ]]; then
      result=$(git -C "$dir" pull --ff-only 2>&1)
      echo "  $result"
      [[ "$result" != *"Already up to date."* ]]
    else
      git clone "$@" "$url" "$dir"
    fi
  }

  # System libraries needed to build C extensions — not Python packages
  APT_PACKAGES=(python3-smbus python3-pip git portaudio19-dev python3-dev i2c-tools)

  if apt_missing "${APT_PACKAGES[@]}"; then
    echo "--- Installing apt packages ---"
    sudo apt-get update
    sudo apt-get install -y "${APT_PACKAGES[@]}"
  else
    echo "--- apt packages already installed, skipping ---"
  fi

  echo "--- Enabling I2C ---"
  sudo raspi-config nonint do_i2c 0

  echo "--- ROS 2 Jazzy + conda environment ---"
  bash "$HOME/install-ros2.sh"

  # install-ros2.sh sets up the conda env — pip installs below go into it
  echo "--- Installing pip packages into conda env ---"
  "$CONDA_PIP" install -q -r "$HOME/requirements.txt"

  echo "--- SunFounder robot-hat ---"
  ROBOT_HAT_DIR="$HOME/robot-hat"
  if git_sync "https://github.com/sunfounder/robot-hat.git" "$ROBOT_HAT_DIR" -b 2.5.x --depth 1; then
    echo "  Changes detected — running install.py..."
    cd "$ROBOT_HAT_DIR"
    sudo python3 install.py
    sudo rm -rf "$ROBOT_HAT_DIR/robot_hat.egg-info" "$ROBOT_HAT_DIR/build"
  else
    echo "  robot-hat source already up to date."
  fi
  "$CONDA_PIP" install -q --force-reinstall "$ROBOT_HAT_DIR"

  echo "--- SunFounder vilib ---"
  VILIB_DIR="$HOME/vilib"
  if git_sync "https://github.com/sunfounder/vilib.git" "$VILIB_DIR"; then
    echo "  Changes detected — running install.py..."
    cd "$VILIB_DIR"
    sudo python3 install.py
  else
    echo "  vilib source already up to date."
  fi
  sudo rm -rf "$VILIB_DIR/build" "$VILIB_DIR/vilib.egg-info"
  "$CONDA_PIP" install -q "$VILIB_DIR"

  echo "--- SunFounder pidog ---"
  PIDOG_DIR="$HOME/pidog"
  if git_sync "https://github.com/sunfounder/pidog.git" "$PIDOG_DIR" --depth 1; then
    echo "  Changes detected."
  else
    echo "  pidog source already up to date."
  fi
  "$CONDA_PIP" install -q "$PIDOG_DIR"

  echo "--- ROS 2 workspace ---"
  bash "$HOME/setup-workspace.sh"

  echo "--- Verifying imports ---"
  "$CONDA_PYTHON" -c "import lgpio; print('  lgpio ok')"
  "$CONDA_PYTHON" -c "import gpiozero; print('  gpiozero ok')"
  "$CONDA_PYTHON" -c "import colorzero; print('  colorzero ok')"
  "$CONDA_PYTHON" -c "from robot_hat import Servo; print('  robot_hat ok')"
  "$CONDA_PYTHON" -c "from pidog import Pidog; print('  pidog ok')"

  echo "--- I2C device scan ---"
  /usr/sbin/i2cdetect -y 1

  echo "--- Done ---"
REMOTE

echo "Pi is ready."
