# Publication review variant; original launcher snapshot: docs/original_launch/.
# enable_yolo defaults to true to preserve the existing launcher default.
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            ExecuteProcess, OpaqueFunction, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def _gz_resource_environment(context, pkg_share):
    extra = LaunchConfiguration('extra_models_path').perform(context)
    existing = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    parts = [os.path.join(pkg_share, 'models'), os.path.join(pkg_share, 'worlds'),
             extra, existing]
    return [SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH',
                                   value=os.pathsep.join(p for p in parts if p))]


def _yolo_process(pkg_share):
    # Avoid hard-coded home directories, venv activation, and bash shell quoting.
    # The Python interpreter must have both ROS Python and ultralytics available.
    return ExecuteProcess(
        cmd=[
            LaunchConfiguration('yolo_python'),
            os.path.join(pkg_share, 'tools', 'yolov8_ros2_node.py'),
            '--ros-args',
            '-p', ['image_topic:=', LaunchConfiguration('camera_image_topic')],
            '-p', ['weights:=', LaunchConfiguration('yolo_weights')],
            '-p', ['conf:=', LaunchConfiguration('yolo_conf')],
            '-p', ['device:=', LaunchConfiguration('yolo_device')],
            '-p', ['rate_hz:=', LaunchConfiguration('yolo_rate_hz')],
            '-p', ['classes:=', LaunchConfiguration('yolo_classes')],
        ],
        output='screen',
        condition=IfCondition(LaunchConfiguration('enable_yolo')),
    )


def _common_arguments(pkg_share, rviz_name):
    return [
        DeclareLaunchArgument('world', default_value=os.path.join(pkg_share, 'worlds', 'house.world'),
                              description='Gazebo Sim .world file to load'),
        DeclareLaunchArgument('extra_models_path', default_value='',
                              description='External Gazebo model directories (parent folder of model names)'),
        DeclareLaunchArgument('bridge_yaml', default_value=os.path.join(pkg_share, 'params', 'tb3_bridge.yaml')),
        DeclareLaunchArgument('urdf', default_value=os.path.join(pkg_share, 'urdf', 'turtlebot3_waffle_pi.urdf')),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        DeclareLaunchArgument('rviz_config', default_value=os.path.join(pkg_share, 'rviz', rviz_name)),
        DeclareLaunchArgument('enable_yolo', default_value='true',
                              description='false for baseline, true for YOLOv8 condition'),
        DeclareLaunchArgument('yolo_python', default_value='python3',
                              description='Python interpreter able to import rclpy, cv_bridge, ultralytics'),
        DeclareLaunchArgument('yolo_weights', default_value='yolov8n.pt',
                              description='Path to verified YOLOv8n weights (not bundled)'),
        DeclareLaunchArgument('camera_image_topic', default_value='/camera/image'),
        DeclareLaunchArgument('yolo_conf', default_value='0.35'),
        DeclareLaunchArgument('yolo_device', default_value='cpu'),
        DeclareLaunchArgument('yolo_rate_hz', default_value='10.0'),
        DeclareLaunchArgument('yolo_classes', default_value='0,56,60'),
    ]


def _common_nodes(pkg_share):
    use_sim_time = ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)
    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                  arguments=['--ros-args', '-p', ['config_file:=', LaunchConfiguration('bridge_yaml')]],
                  parameters=[{'use_sim_time': use_sim_time}], output='screen')
    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               parameters=[{'use_sim_time': use_sim_time,
                            'robot_description': ParameterValue(
                                Command(['xacro ', LaunchConfiguration('urdf')]), value_type=str)}],
               output='screen')
    rviz = Node(package='rviz2', executable='rviz2',
                arguments=['-d', LaunchConfiguration('rviz_config')],
                parameters=[{'use_sim_time': use_sim_time}], output='screen',
                condition=IfCondition(LaunchConfiguration('use_rviz')))
    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'),
                                                   'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r ', LaunchConfiguration('world')]}.items())
    return gz, bridge, rsp, rviz

def generate_launch_description():
    pkg_share = get_package_share_directory('tb3_gmapping_demo')
    gz, bridge, rsp, rviz = _common_nodes(pkg_share)
    cartographer = Node(
        package='cartographer_ros', executable='cartographer_node', name='cartographer_node',
        parameters=[{'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool)}],
        arguments=['-configuration_directory', LaunchConfiguration('cartographer_config_dir'),
                   '-configuration_basename', LaunchConfiguration('configuration_basename')],
        remappings=[('scan', '/scan')], output='screen')
    occupancy = Node(
        package='cartographer_ros', executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node', output='screen',
        parameters=[{'use_sim_time': ParameterValue(LaunchConfiguration('use_sim_time'), value_type=bool),
                     'resolution': ParameterValue(LaunchConfiguration('resolution'), value_type=float),
                     'publish_period_sec': ParameterValue(LaunchConfiguration('publish_period_sec'), value_type=float)}])
    carto_args = [
        DeclareLaunchArgument('cartographer_config_dir', default_value=os.path.join(pkg_share, 'config')),
        DeclareLaunchArgument('configuration_basename', default_value='tb3_cartographer.lua'),
        DeclareLaunchArgument('resolution', default_value='0.05'),
        DeclareLaunchArgument('publish_period_sec', default_value='1.0'),
    ]
    return LaunchDescription(
        _common_arguments(pkg_share, 'cartographer.rviz') + carto_args +
        [OpaqueFunction(function=_gz_resource_environment, args=[pkg_share]),
         gz, bridge, rsp, cartographer, occupancy, rviz, _yolo_process(pkg_share)])
