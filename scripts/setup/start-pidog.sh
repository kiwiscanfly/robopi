#!/usr/bin/env bash
# Launcher for the pidog systemd service.
# Deployed to ~/start-pidog.sh by setup-service.sh.
set +u
source /home/rebecca/miniforge3/etc/profile.d/conda.sh
conda activate ros_env
source /home/rebecca/ros2_ws/install/setup.bash
set -u
exec ros2 launch pidog_ros2 pidog.launch.py
