import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory("tb3_gmapping_demo")

    world_file = os.path.join(pkg_share, "worlds", "house.world")
    bridge_yaml = os.path.join(pkg_share, "params", "tb3_bridge.yaml")
    frames_urdf = os.path.join(pkg_share, "urdf", "turtlebot3_waffle_pi.urdf")

    # RViz config (optional)
    rviz_config = os.path.join(pkg_share, "rviz", "gmapping.rviz")

    # Make Gazebo Sim find your package models
    existing_gz_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    pkg_models_path = os.path.join(pkg_share, "models")
    pkg_worlds_path = os.path.join(pkg_share, "worlds")
    combined_gz_path = ":".join([p for p in [pkg_models_path, pkg_worlds_path, existing_gz_path] if p])

    set_gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=combined_gz_path
    )

    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={"gz_args": f"-r {world_file}"}.items(),
    )

    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["--ros-args", "-p", f"config_file:={bridge_yaml}"],
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    with open(frames_urdf, "r") as f:
        robot_description = f.read()

    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": True,
            "robot_description": robot_description
        }],
    )

    # GMapping
    gmapping_node = Node(
        package="slam_gmapping",
        executable="slam_gmapping",
        name="slam_gmapping",
        output="screen",
        parameters=[{
            "use_sim_time": True,
            "base_frame": "base_footprint",
            "odom_frame": "odom",
            "map_frame": "map",
        }],
        remappings=[("scan", "/scan")],
    )

    # RViz
    rviz_args = ["-d", rviz_config] if os.path.exists(rviz_config) else []
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=rviz_args,
        parameters=[{"use_sim_time": True}],
    )

    # ✅ YOLOv8 auto-start (runs in your venv)
    home = os.path.expanduser("~")
    ws_setup = os.path.join(home, "gmapping_ws", "install", "setup.bash")
    venv_activate = os.path.join(home, "gmapping_ws", "yolo_venv", "bin", "activate")
    yolo_script = os.path.join(home, "gmapping_ws", "tools", "yolov8_ros2_node.py")

    # Detect: person(0), chair(56), dining table(60)
    yolo_cmd = (
        f"source /opt/ros/jazzy/setup.bash; "
        f"source {ws_setup}; "
        f"source {venv_activate}; "
        f"python3 {yolo_script} --ros-args "
        f"-p image_topic:=/camera/image "
        f"-p weights:=yolov8n.pt "
        f"-p conf:=0.35 "
        f"-p device:=cpu "
        f"-p rate_hz:=10.0 "
        f"-p classes:='0,56,60'"
    )

    yolo_process = ExecuteProcess(
        cmd=["bash", "-lc", yolo_cmd],
        output="screen",
    )

    return LaunchDescription([
        set_gz_resource_path,
        gz_launch,
        bridge_node,
        rsp_node,
        gmapping_node,
        rviz_node,
        yolo_process,
    ])