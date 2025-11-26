import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    package_dir = get_package_share_directory('livox_ros_driver2')
    config_path = os.path.join(package_dir, 'config', 'MID360_config.json')

    livox_driver = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_lidar_publisher',
        output='screen',
        parameters=[
            {"xfer_format": 0},         # PointCloud2 (XYZRTL)
            {"multi_topic": 0},         # Single topic
            {"data_src": 0},            # LiDAR
            {"publish_freq": 10.0},
            {"output_data_type": 0},    # ROS PointCloud2
            {"frame_id": "livox_frame"},
            {"user_config_path": config_path},
            {"start_mode": 1}           # <-- WAJIB! tanpa ini tidak streaming
        ]
    )

    tf_pub = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='livox_tf_pub',
        arguments=['0', '0', '0', '0', '0', '0', 'livox_frame', 'base_link']
    )

    return LaunchDescription([livox_driver, tf_pub])

