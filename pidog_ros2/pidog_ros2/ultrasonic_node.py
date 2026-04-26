#!/usr/bin/env python3
# Publishes ultrasonic distance readings from the PiDog to /pidog/ultrasonic.
# Message type: sensor_msgs/Range

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range
from pidog import Pidog
from robot_hat.music import disable_speaker
import math


PUBLISH_RATE_HZ = 10
MIN_RANGE_M = 0.02   # 2 cm
MAX_RANGE_M = 4.0    # 400 cm


class UltrasonicNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_node')
        self.publisher = self.create_publisher(Range, '/pidog/ultrasonic', 10)
        self.dog = Pidog()
        disable_speaker()
        self.timer = self.create_timer(1.0 / PUBLISH_RATE_HZ, self.publish_reading)
        self.get_logger().info('Ultrasonic node started, publishing on /pidog/ultrasonic')

    def publish_reading(self):
        distance_cm = self.dog.ultrasonic.read()
        if distance_cm is None:
            return

        msg = Range()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'ultrasonic'
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = 0.26  # ~15 degrees in radians
        msg.min_range = MIN_RANGE_M
        msg.max_range = MAX_RANGE_M
        msg.range = distance_cm / 100.0  # convert cm to metres

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
