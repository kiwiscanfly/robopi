#!/usr/bin/env bash
# Verify that all Python packages import correctly and I2C devices are visible.
# Runs on the Pi — called by setup-pi.sh or directly: bash ~/verify.sh

set -euo pipefail

CONDA_PYTHON="$HOME/miniforge3/envs/ros_env/bin/python3"

echo "--- Verifying imports ---"
"$CONDA_PYTHON" -c "import lgpio; print('  lgpio ok')"
"$CONDA_PYTHON" -c "import gpiozero; print('  gpiozero ok')"
"$CONDA_PYTHON" -c "import colorzero; print('  colorzero ok')"
"$CONDA_PYTHON" -c "from robot_hat import Servo; print('  robot_hat ok')"
"$CONDA_PYTHON" -c "from pidog import Pidog; print('  pidog ok')"

echo "--- I2C device scan ---"
/usr/sbin/i2cdetect -y 1
