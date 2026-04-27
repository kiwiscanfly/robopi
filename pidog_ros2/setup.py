from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'pidog_ros2'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rebecca Milne',
    maintainer_email='rebecca@bex.codes',
    description='ROS 2 nodes wrapping the SunFounder PiDog v2',
    license='MIT',
    entry_points={
        'console_scripts': [
            'pidog_node = pidog_ros2.pidog_node:main',
            'camera_node = pidog_ros2.camera_node:main',
        ],
    },
)
