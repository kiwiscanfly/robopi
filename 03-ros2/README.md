# Stage 3 — ROS 2 Integration

This stage wraps the PiDog v2 in ROS 2 Jazzy nodes, creating a data pipeline
from sensors through to actuators that will serve as the foundation for ML
experimentation in Stage 4.

## Architecture

```
Sensors                         Topics                      Actuators
──────────────────────────────────────────────────────────────────────
ultrasonic_node  →  /pidog/ultrasonic  (sensor_msgs/Range)
imu_node         →  /pidog/imu         (sensor_msgs/Imu)
touch_node       →  /pidog/touch       (std_msgs/String)
camera_node      →  /pidog/camera/image_raw  (sensor_msgs/Image)
                    /pidog/cmd_vel     (geometry_msgs/Twist)   →  movement_node
                    /pidog/cmd_action  (std_msgs/String)       →  movement_node
```

## Setup

ROS 2 is installed and the workspace is built automatically by `setup-pi.sh`.
To run it manually on the Pi:

```bash
# Install ROS 2 Jazzy
bash ~/install-ros2.sh

# Build the workspace
bash ~/setup-workspace.sh
```

## Running

Start all nodes with the launch file:

```bash
source ~/.bashrc
ros2 launch pidog_ros2 pidog.launch.py
```

Or run individual nodes for testing:

```bash
ros2 run pidog_ros2 ultrasonic_node
```

## Verifying

From the Pi (or another machine on the same network with ROS_DOMAIN_ID set):

```bash
# List all active topics
ros2 topic list

# Check ultrasonic publish rate
ros2 topic hz /pidog/ultrasonic

# Watch distance values
ros2 topic echo /pidog/ultrasonic

# Make the dog sit
ros2 topic pub --once /pidog/cmd_action std_msgs/String "data: 'sit'"
```

## Nodes

| Node | Package | Topic(s) |
|------|---------|----------|
| `ultrasonic_node` | `pidog_ros2` | `/pidog/ultrasonic` |
| `imu_node` | `pidog_ros2` | `/pidog/imu` |
| `touch_node` | `pidog_ros2` | `/pidog/touch` |
| `camera_node` | `pidog_ros2` | `/pidog/camera/image_raw` |
| `movement_node` | `pidog_ros2` | `/pidog/cmd_vel`, `/pidog/cmd_action` |

## Stage 4 Preview — ML Integration

Each ML use case will be a ROS 2 node that subscribes to sensor topics:

- **Computer vision** — `vision_node` wraps vilib detections → `/pidog/vision/detections`
- **Sensor fusion** — `fusion_node` combines IMU + ultrasonic + touch → `/pidog/state`
- **Reinforcement learning** — record rosbags as datasets, deploy trained policy as a node
- **LLM / voice control** — `voice_node` wraps Ollama/GPT → `/pidog/cmd_action`
