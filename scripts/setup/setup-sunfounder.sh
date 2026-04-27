#!/usr/bin/env bash
# Install SunFounder libraries: robot-hat, vilib, pidog into the conda env.
# Runs on the Pi — called by setup-pi.sh or directly: bash ~/setup-sunfounder.sh

set -euo pipefail

CONDA_PIP="$HOME/miniforge3/envs/ros_env/bin/pip"

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

echo "--- SunFounder robot-hat ---"
ROBOT_HAT_DIR="$HOME/robot-hat"
if ! "$CONDA_PIP" show robot-hat &>/dev/null || \
   git_sync "https://github.com/sunfounder/robot-hat.git" "$ROBOT_HAT_DIR" -b 2.5.x --depth 1; then
  echo "  Installing robot-hat..."
  cd "$ROBOT_HAT_DIR"
  sudo python3 install.py
  sudo rm -rf "$ROBOT_HAT_DIR/robot_hat.egg-info" "$ROBOT_HAT_DIR/build"
  "$CONDA_PIP" install -q --force-reinstall "$ROBOT_HAT_DIR"
else
  echo "  robot-hat already up to date."
fi

echo "--- SunFounder vilib ---"
VILIB_DIR="$HOME/vilib"
if ! "$CONDA_PIP" show vilib &>/dev/null || \
   git_sync "https://github.com/sunfounder/vilib.git" "$VILIB_DIR"; then
  echo "  Installing vilib..."
  cd "$VILIB_DIR"
  sudo python3 install.py
  sudo rm -rf "$VILIB_DIR/build" "$VILIB_DIR/vilib.egg-info"
  "$CONDA_PIP" install -q "$VILIB_DIR"
else
  echo "  vilib already up to date."
fi

echo "--- SunFounder pidog ---"
PIDOG_DIR="$HOME/pidog"
if ! "$CONDA_PIP" show pidog &>/dev/null || \
   git_sync "https://github.com/sunfounder/pidog.git" "$PIDOG_DIR" --depth 1; then
  echo "  Installing pidog..."
  "$CONDA_PIP" install -q "$PIDOG_DIR"
else
  echo "  pidog already up to date."
fi

echo "--- SunFounder libraries complete ---"
