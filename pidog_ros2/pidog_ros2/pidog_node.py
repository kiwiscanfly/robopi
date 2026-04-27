#!/usr/bin/env python3
# Unified PiDog driver node — owns the single Pidog() instance and exposes
# all sensors and actuators as ROS 2 topics.
#
# Having one node own the Pidog instance is critical: if multiple nodes each
# create a Pidog(), they run in separate OS processes and will conflict over
# the shared I2C, SPI, and GPIO hardware.
#
# Publishers:
#   /pidog/ultrasonic        sensor_msgs/Range      10 Hz
#   /pidog/imu               sensor_msgs/Imu        50 Hz
#   /pidog/touch             std_msgs/String        on change
#   /pidog/sound_direction   std_msgs/Float32       10 Hz
#   /pidog/battery           std_msgs/Float32        1 Hz
#
# Subscribers:
#   /pidog/cmd_vel           geometry_msgs/Twist    walking velocity
#   /pidog/cmd_action        std_msgs/String        named action
#   /pidog/cmd_head          geometry_msgs/Vector3  head roll/pitch/yaw (degrees)
#   /pidog/cmd_led           std_msgs/String        "style:color" e.g. "breath:blue"

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range, Imu
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist, Vector3
from pidog import Pidog
from robot_hat.music import disable_speaker


VALID_ACTIONS = {
    # Locomotion
    'forward', 'backward', 'turn_left', 'turn_right', 'trot',
    # Postures
    'stand', 'sit', 'lie', 'lie_with_hands_out', 'half_sit',
    # Head / body movements
    'stretch', 'push_up', 'doze_off', 'wag_tail', 'head_up_down',
    'nod_lethargy', 'shake_head', 'tilting_head_left', 'tilting_head_right',
    'tilting_head', 'head_bark',
    # Preset behaviours
    'scratch', 'hand_shake', 'high_five', 'pant', 'body_twisting',
    'bark_action', 'bark', 'shake_head_smooth', 'howling', 'attack_posture',
    'lick_hand', 'waiting', 'feet_shake', 'sit_2_stand', 'relax_neck',
    'nod', 'think', 'recall', 'head_down_left', 'head_down_right',
    'fluster', 'alert', 'surprise',
}

DEADZONE = 0.05

ULTRASONIC_MIN_M = 0.02
ULTRASONIC_MAX_M = 4.0
ULTRASONIC_FOV_RAD = 0.26  # ~15 degrees


class PidogNode(Node):
    def __init__(self):
        super().__init__('pidog_node')

        self.dog = Pidog()
        disable_speaker()

        # Publishers
        self.pub_ultrasonic = self.create_publisher(Range, '/pidog/ultrasonic', 10)
        self.pub_imu = self.create_publisher(Imu, '/pidog/imu', 10)
        self.pub_touch = self.create_publisher(String, '/pidog/touch', 10)
        self.pub_sound_dir = self.create_publisher(Float32, '/pidog/sound_direction', 10)
        self.pub_battery = self.create_publisher(Float32, '/pidog/battery', 10)

        # Subscribers
        self.create_subscription(Twist, '/pidog/cmd_vel', self.on_cmd_vel, 10)
        self.create_subscription(String, '/pidog/cmd_action', self.on_cmd_action, 10)
        self.create_subscription(Vector3, '/pidog/cmd_head', self.on_cmd_head, 10)
        self.create_subscription(String, '/pidog/cmd_led', self.on_cmd_led, 10)

        # Timers
        self.create_timer(0.1,  self.publish_ultrasonic)   # 10 Hz
        self.create_timer(0.02, self.publish_imu)          # 50 Hz
        self.create_timer(0.05, self.publish_touch)        # 20 Hz
        self.create_timer(0.1,  self.publish_sound_dir)    # 10 Hz
        self.create_timer(1.0,  self.publish_battery)      #  1 Hz

        self._last_touch = 'N'
        self._battery_ok = True

        self.get_logger().info('PiDog node started')
        self.get_logger().info('  Publishers: /pidog/ultrasonic, /pidog/imu, /pidog/touch, '
                               '/pidog/sound_direction, /pidog/battery')
        self.get_logger().info('  Subscribers: /pidog/cmd_vel, /pidog/cmd_action, '
                               '/pidog/cmd_head, /pidog/cmd_led')

    # ── Publishers ────────────────────────────────────────────────────────────

    def publish_ultrasonic(self):
        distance_cm = self.dog.ultrasonic.read()
        if distance_cm is None:
            return
        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'ultrasonic'
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = ULTRASONIC_FOV_RAD
        msg.min_range = ULTRASONIC_MIN_M
        msg.max_range = ULTRASONIC_MAX_M
        msg.range = distance_cm / 100.0
        self.pub_ultrasonic.publish(msg)

    def publish_imu(self):
        try:
            ax, ay, az = self.dog.accData
            gx, gy, gz = self.dog.gyroData
        except Exception as e:
            self.get_logger().warn(f'IMU read failed: {e}')
            return
        g = 9.80665
        deg_to_rad = math.pi / 180.0
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu'
        msg.linear_acceleration.x = ax * g
        msg.linear_acceleration.y = ay * g
        msg.linear_acceleration.z = az * g
        msg.angular_velocity.x = gx * deg_to_rad
        msg.angular_velocity.y = gy * deg_to_rad
        msg.angular_velocity.z = gz * deg_to_rad
        msg.orientation_covariance[0] = -1.0  # orientation not provided
        self.pub_imu.publish(msg)

    def publish_touch(self):
        state = self.dog.dual_touch.read()
        if state != self._last_touch:
            msg = String()
            msg.data = state
            self.pub_touch.publish(msg)
            self._last_touch = state

    def publish_sound_dir(self):
        angle = self.dog.ears.read()
        msg = Float32()
        msg.data = float(angle)  # 0–359 degrees, or -1 if no detection
        self.pub_sound_dir.publish(msg)

    def publish_battery(self):
        if not self._battery_ok:
            return
        try:
            voltage = self.dog.get_battery_voltage()
            msg = Float32()
            msg.data = float(voltage)
            self.pub_battery.publish(msg)
        except Exception as e:
            self.get_logger().warn(f'Battery read failed: {e} — disabling battery publisher')
            self._battery_ok = False

    # ── Subscribers ───────────────────────────────────────────────────────────

    def on_cmd_vel(self, msg: Twist):
        forward = msg.linear.x
        turn = msg.angular.z

        if abs(forward) >= DEADZONE:
            action = 'forward' if forward > 0 else 'backward'
            speed = min(100, int(abs(forward) * 100))
            self.dog.do_action(action, step_count=1, speed=speed)
        elif abs(turn) >= DEADZONE:
            action = 'turn_left' if turn > 0 else 'turn_right'
            speed = min(100, int(abs(turn) * 100))
            self.dog.do_action(action, step_count=1, speed=speed)
        else:
            self.dog.do_action('stand', speed=80)

    def on_cmd_action(self, msg: String):
        action = msg.data.strip().lower()
        if action not in VALID_ACTIONS:
            self.get_logger().warn(f"Unknown action '{action}'. Valid: {sorted(VALID_ACTIONS)}")
            return
        self.get_logger().info(f'Action: {action}')
        self.dog.do_action(action, speed=80)

    def on_cmd_head(self, msg: Vector3):
        roll = msg.x
        pitch = msg.y
        yaw = msg.z
        self.get_logger().info(f'Head move: roll={roll} pitch={pitch} yaw={yaw}')
        self.dog.head_move([[roll, pitch, yaw]], speed=80)

    def on_cmd_led(self, msg: String):
        parts = msg.data.strip().split(':')
        style = parts[0] if len(parts) > 0 else 'monochromatic'
        color = parts[1] if len(parts) > 1 else 'white'
        self.get_logger().info(f'LED: style={style} color={color}')
        self.dog.rgb_strip.set_mode(style=style, color=color, bps=1, brightness=0.8)

    def destroy_node(self):
        self.dog.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = PidogNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
