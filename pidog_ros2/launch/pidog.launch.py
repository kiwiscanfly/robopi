import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess


WEBUI_DIR = os.path.expanduser('~/pidog_webui')
WEBUI_PORT = '8000'


def generate_launch_description():
    return LaunchDescription([
        Node(package='pidog_ros2', executable='pidog_node',  name='pidog_node'),
        Node(package='pidog_ros2', executable='camera_node', name='camera_node'),
        Node(package='rosbridge_server', executable='rosbridge_websocket',
             name='rosbridge_ws', parameters=[{'port': 9090}]),
        ExecuteProcess(
            cmd=['python3', '-m', 'http.server', WEBUI_PORT, '--directory', WEBUI_DIR],
            name='webui_server',
            output='screen',
        ),
    ])
