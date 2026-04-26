#!/usr/bin/env python3
# Publishes dual touch sensor state from the PiDog to /pidog/touch.
# Message type: std_msgs/String
# Values: N (none), L (left), R (right), LS (left-to-right slide), RS (right-to-left slide)

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pidog import Pidog


PUBLISH_RATE_HZ = 20


class TouchNode(Node):
    def __init__(self):
        super().__init__('touch_node')
        self.publisher = self.create_publisher(String, '/pidog/touch', 10)
        self.dog = Pidog()
        self.dog.music.music_stop()
        self.dog.music.music_set_volume(0)
        self.last_state = 'N'
        self.timer = self.create_timer(1.0 / PUBLISH_RATE_HZ, self.publish_reading)
        self.get_logger().info('Touch node started, publishing on /pidog/touch')

    def publish_reading(self):
        state = self.dog.dual_touch.read()

        # Only publish on state change to avoid flooding subscribers
        if state != self.last_state:
            msg = String()
            msg.data = state
            self.publisher.publish(msg)
            self.last_state = state


def main(args=None):
    rclpy.init(args=args)
    node = TouchNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
