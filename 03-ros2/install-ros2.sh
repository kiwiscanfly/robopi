#!/usr/bin/env bash
# Install ROS 2 Jazzy via RoboStack (conda-based) on Raspberry Pi OS Bookworm.
# Called by scripts/setup-pi.sh — not intended to be run directly.
#
# Why RoboStack instead of apt:
# The official ROS 2 Jazzy apt packages target Ubuntu Noble (Python 3.12,
# GCC 13, glibc 2.38). Bookworm has older versions of all three and the
# packages simply won't install. RoboStack ships pre-compiled conda packages
# that are independent of system libraries, resolving in minutes.

set -euo pipefail

CONDA_DIR="$HOME/miniforge3"
ROS_ENV="ros_env"

echo "--- Installing ROS 2 Jazzy via RoboStack ---"

# Install Miniforge if not already present
if [[ ! -d "$CONDA_DIR" ]]; then
  echo "  Installing Miniforge..."
  MINIFORGE_INSTALLER="$HOME/Miniforge3-installer.sh"
  curl -fsSL "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh" \
    -o "$MINIFORGE_INSTALLER"
  bash "$MINIFORGE_INSTALLER" -b -p "$CONDA_DIR"
  rm "$MINIFORGE_INSTALLER"
  echo "  Miniforge installed at $CONDA_DIR"
else
  echo "  Miniforge already installed."
fi

# RoboStack's activation scripts reference several variables that aren't set in
# non-interactive shells. set +u/-u scopes the relaxation as tightly as possible.
set +u
source "$CONDA_DIR/etc/profile.d/conda.sh"

if ! conda env list | grep -q "^$ROS_ENV "; then
  echo "  Creating conda environment '$ROS_ENV'..."
  conda create -n "$ROS_ENV" -y python=3.11
fi

conda activate "$ROS_ENV"
set -u

# Configure RoboStack channels
conda config --env --add channels conda-forge
conda config --env --add channels robostack-jazzy
conda config --env --set channel_priority strict

# Install ROS 2 Jazzy base if not already installed
if ! conda list -n "$ROS_ENV" | grep -q "^ros-jazzy-ros-base "; then
  echo "  Installing ros-jazzy-ros-base (this may take a few minutes)..."
  mamba install -y ros-jazzy-ros-base
else
  echo "  ros-jazzy-ros-base already installed."
fi

# Install colcon if not present
if ! conda list -n "$ROS_ENV" | grep -q "^colcon-common-extensions "; then
  echo "  Installing colcon..."
  mamba install -y colcon-common-extensions
else
  echo "  colcon already installed."
fi

# Add conda activation + ROS 2 source to .bashrc if not already there
if ! grep -q "ros_env" "$HOME/.bashrc"; then
  cat >> "$HOME/.bashrc" <<'BASHRC'

# ROS 2 (RoboStack)
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate ros_env
source "$HOME/miniforge3/envs/ros_env/setup.bash"
BASHRC
  echo "  Added ROS 2 activation to ~/.bashrc"
fi

echo "  ROS 2 Jazzy (RoboStack) installation complete."
echo "  Run 'source ~/.bashrc' or open a new shell to activate."
