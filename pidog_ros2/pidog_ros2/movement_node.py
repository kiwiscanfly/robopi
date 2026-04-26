#!/usr/bin/env python3
# Subscribes to movement commands and translates them to PiDog actions.
#
# Topics:
#   /pidog/cmd_vel  (geometry_msgs/Twist)  — forward/back/turn
#   /pidog/cmd_action (std_msgs/String)    — named actions: sit, stand, wave,
#                                            shake_hands, howl, stretch, push_up

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from pidog import Pidog
from robot_hat.music import disable_speaker
import time


# Maps action name strings to pidog method calls
ACTION_MAP = {
    'sit':          lambda dog: dog.do_action('sit', speed=80),
    'stand':        lambda dog: dog.do_action('stand', speed=80),
    'wave':         lambda dog: dog.do_action('wave', speed=80),
    'shake_hands':  lambda dog: dog.do_action('shake_hands', speed=80),
    'howl':         lambda dog: dog.do_action('howl', speed=80),
    'stretch':      lambda dog: dog.do_action('stretch', speed=80),
    'push_up':      lambda dog: dog.do_action('push_up', speed=80),
}

# Velocity threshold below which we treat the command as stop
DEADZONE = 0.05


class MovementNode(Node):
    def __init__(self):
        super().__init__('movement_node')
        self.dog = Pidog()
        disable_speaker()

        self.cmd_vel_sub = self.create_subscription(
            Twist, '/pidog/cmd_vel', self.on_cmd_vel, 10)
        self.cmd_action_sub = self.create_subscription(
            String, '/pidog/cmd_action', self.on_cmd_action, 10)

        self.get_logger().info('Movement node started')
        self.get_logger().info('  /pidog/cmd_vel  — Twist (linear.x, angular.z)')
        self.get_logger().info(f'  /pidog/cmd_action — String: {list(ACTION_MAP.keys())}')

    def on_cmd_vel(self, msg: Twist):
        forward = msg.linear.x
        turn = msg.angular.z

        if abs(forward) < DEADZONE and abs(turn) < DEADZONE:
            self.dog.do_action('stand', speed=80)
            return

        step_len = int(forward * 40)  # scale to pidog step length range
        angle = int(-turn * 30)       # scale to pidog turn angle range

        self.dog.do_action('forward', step_count=1, speed=80)

    def on_cmd_action(self, msg: String):
        action = msg.data.strip().lower()
        if action not in ACTION_MAP:
            self.get_logger().warn(
                f"Unknown action '{action}'. Valid actions: {list(ACTION_MAP.keys())}")
            return
        self.get_logger().info(f"Executing action: {action}")
        ACTION_MAP[action](self.dog)


def main(args=None):
    rclpy.init(args=args)
    node = MovementNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
