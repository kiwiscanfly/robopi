# Stage 3 — ROS 2 Integration

This stage wraps the PiDog v2 in ROS 2 Jazzy nodes, creating a data pipeline
from sensors through to actuators that will serve as the foundation for ML
experimentation in Stage 4.

## Architecture

A single `pidog_node` owns the `Pidog()` hardware instance. This avoids I2C/SPI
conflicts that would occur if multiple nodes each created their own `Pidog()`.
The `camera_node` is separate since it uses vilib, not pidog directly.

```
pidog_node
  publishes →  /pidog/ultrasonic       (sensor_msgs/Range)      10 Hz
  publishes →  /pidog/imu              (sensor_msgs/Imu)        50 Hz
  publishes →  /pidog/touch            (std_msgs/String)        on change
  publishes →  /pidog/sound_direction  (std_msgs/Float32)       10 Hz
  publishes →  /pidog/battery          (std_msgs/Float32)        1 Hz
  subscribes ← /pidog/cmd_vel          (geometry_msgs/Twist)
  subscribes ← /pidog/cmd_action       (std_msgs/String)
  subscribes ← /pidog/cmd_head         (geometry_msgs/Vector3)
  subscribes ← /pidog/cmd_led          (std_msgs/String)

camera_node
  publishes →  /pidog/camera/image_raw (sensor_msgs/Image)      15 Hz
```

## Setup

ROS 2 is installed and the workspace is built automatically by `setup-pi.sh`.
To run individual steps manually on the Pi:

```bash
bash ~/install-ros2.sh      # install ROS 2 via RoboStack
bash ~/setup-workspace.sh   # build the colcon workspace
```

## Running

Start both nodes with the launch file:

```bash
source ~/.bashrc
ros2 launch pidog_ros2 pidog.launch.py
```

Or run a single node for testing:

```bash
ros2 run pidog_ros2 pidog_node
```

## Verifying

```bash
# List all active topics
ros2 topic list

# Check sensor rates
ros2 topic hz /pidog/ultrasonic       # ~10 Hz
ros2 topic hz /pidog/imu              # ~50 Hz

# Watch sensor values
ros2 topic echo /pidog/ultrasonic
ros2 topic echo /pidog/battery
ros2 topic echo /pidog/sound_direction

# Control the dog
ros2 topic pub --once /pidog/cmd_action std_msgs/String "data: 'sit'"
ros2 topic pub --once /pidog/cmd_action std_msgs/String "data: 'stand'"
ros2 topic pub --once /pidog/cmd_head geometry_msgs/Vector3 "{x: 0.0, y: 20.0, z: 0.0}"
ros2 topic pub --once /pidog/cmd_led std_msgs/String "data: 'breath:blue'"
ros2 topic pub /pidog/cmd_vel geometry_msgs/Twist "{linear: {x: 0.5}}" --rate 5
```

## Valid actions for /pidog/cmd_action

**Locomotion:** `forward`, `backward`, `turn_left`, `turn_right`, `trot`
**Postures:** `stand`, `sit`, `lie`, `lie_with_hands_out`, `half_sit`
**Head/body:** `stretch`, `push_up`, `doze_off`, `wag_tail`, `head_up_down`, `nod_lethargy`, `shake_head`, `tilting_head_left`, `tilting_head_right`, `tilting_head`, `head_bark`
**Preset behaviours:** `scratch`, `hand_shake`, `high_five`, `pant`, `body_twisting`, `bark_action`, `bark`, `shake_head_smooth`, `howling`, `attack_posture`, `lick_hand`, `waiting`, `feet_shake`, `sit_2_stand`, `relax_neck`, `nod`, `think`, `recall`, `head_down_left`, `head_down_right`, `fluster`, `alert`, `surprise`

## Stage 4 Preview — ML Integration

Each ML use case will be a ROS 2 node that subscribes to sensor topics:

- **Computer vision** — `vision_node` wraps vilib detections → `/pidog/vision/detections`
- **Sensor fusion** — `fusion_node` combines IMU + ultrasonic + touch → `/pidog/state`
- **Reinforcement learning** — record rosbags as datasets, deploy trained policy as a node
- **LLM / voice control** — `voice_node` wraps Ollama/GPT → `/pidog/cmd_action`
