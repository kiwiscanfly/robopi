from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(package='pidog_ros2', executable='ultrasonic_node', name='ultrasonic_node'),
        Node(package='pidog_ros2', executable='imu_node',        name='imu_node'),
        Node(package='pidog_ros2', executable='touch_node',      name='touch_node'),
        Node(package='pidog_ros2', executable='camera_node',     name='camera_node'),
        Node(package='pidog_ros2', executable='movement_node',   name='movement_node'),
    ])
