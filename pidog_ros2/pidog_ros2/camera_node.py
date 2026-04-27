#!/usr/bin/env python3
# Publishes camera frames from the PiDog to /pidog/camera/image_raw.
# Message type: sensor_msgs/Image

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from vilib import Vilib
import numpy as np


PUBLISH_RATE_HZ = 15
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.publisher = self.create_publisher(Image, '/pidog/camera/image_raw', 10)
        Vilib.camera_start(vflip=False, hflip=False)
        Vilib.display(local=False, web=True)
        self.timer = self.create_timer(1.0 / PUBLISH_RATE_HZ, self.publish_frame)
        self.get_logger().info('Camera node started — ROS topic: /pidog/camera/image_raw'
                               ' — web stream: http://robopi.local:9000/mjpg')

    def publish_frame(self):
        raw = Vilib.img
        if raw is None or len(raw) == 0 or raw[0] is None:
            return

        frame = np.array(raw[0], dtype=np.uint8)

        if frame.ndim != 3:
            return

        msg = Image()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera'
        msg.height = frame.shape[0]
        msg.width = frame.shape[1]
        msg.encoding = 'bgr8'
        msg.step = frame.shape[1] * 3
        msg.data = frame.tobytes()
        self.publisher.publish(msg)

    def destroy_node(self):
        Vilib.camera_close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CameraNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
