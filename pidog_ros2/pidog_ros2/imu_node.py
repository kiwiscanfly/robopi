#!/usr/bin/env python3
# Publishes IMU data from the PiDog SH3001 to /pidog/imu.
# Message type: sensor_msgs/Imu

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from pidog import Pidog
import math


PUBLISH_RATE_HZ = 50  # IMU benefits from higher rate


class ImuNode(Node):
    def __init__(self):
        super().__init__('imu_node')
        self.publisher = self.create_publisher(Imu, '/pidog/imu', 10)
        self.dog = Pidog()
        self.dog.music.music_stop()
        self.dog.music.music_set_volume(0)
        self.timer = self.create_timer(1.0 / PUBLISH_RATE_HZ, self.publish_reading)
        self.get_logger().info('IMU node started, publishing on /pidog/imu')

    def publish_reading(self):
        try:
            ax, ay, az = self.dog.accData
            gx, gy, gz = self.dog.gyroData
        except Exception as e:
            self.get_logger().warn(f'IMU read failed: {e}')
            return

        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu'

        # Linear acceleration in m/s² (sensor returns g, convert to m/s²)
        g = 9.80665
        msg.linear_acceleration.x = ax * g
        msg.linear_acceleration.y = ay * g
        msg.linear_acceleration.z = az * g

        # Angular velocity in rad/s (sensor returns degrees/s)
        deg_to_rad = math.pi / 180.0
        msg.angular_velocity.x = gx * deg_to_rad
        msg.angular_velocity.y = gy * deg_to_rad
        msg.angular_velocity.z = gz * deg_to_rad

        # Orientation unknown — mark covariance as -1 (not provided)
        msg.orientation_covariance[0] = -1.0

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ImuNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
