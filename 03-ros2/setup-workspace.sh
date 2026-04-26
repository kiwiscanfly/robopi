#!/usr/bin/env bash
# Set up the ROS 2 colcon workspace on the Pi and build the pidog_ros2 package.
# Called by scripts/setup-pi.sh — not intended to be run directly.

set -euo pipefail

WORKSPACE="$HOME/ros2_ws"
PACKAGE_SRC="$HOME/pidog_ros2"

echo "--- Setting up ROS 2 workspace ---"

set +u
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate ros_env
set -u

mkdir -p "$WORKSPACE/src"

# Symlink the package into the workspace
if [[ ! -L "$WORKSPACE/src/pidog_ros2" ]]; then
  echo "  Linking pidog_ros2 package into workspace..."
  ln -s "$PACKAGE_SRC" "$WORKSPACE/src/pidog_ros2"
fi

echo "  Building workspace with colcon..."
cd "$WORKSPACE"
colcon build

# Add workspace overlay to .bashrc if not already there
if ! grep -q "source $WORKSPACE/install/setup.bash" "$HOME/.bashrc"; then
  echo "source $WORKSPACE/install/setup.bash" >> "$HOME/.bashrc"
  echo "  Added workspace overlay to ~/.bashrc"
fi

echo "  Workspace built. Run: source ~/ros2_ws/install/setup.bash"
