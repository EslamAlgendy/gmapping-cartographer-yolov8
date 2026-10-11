import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.substitutions import Command, TextSubstitution
from launch.actions import ExecuteProcess



def generate_launch_description():
    pkg_share = get_package_share_directory("tb3_gmapping_demo")

    # -----------------------------
    # Launch arguments
    # -----------------------------
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    use_rviz = LaunchConfiguration("use_rviz", default="true")

    cartographer_config_dir = LaunchConfiguration(
        "cartographer_config_dir",
        default=os.path.join(pkg_share, "config"),
    )
    configuration_basename = LaunchConfiguration(
        "configuration_basename",
        default="tb3_cartographer.lua",
    )

    resolution = LaunchConfiguration("resolution", default="0.05")
    publish_period_sec = LaunchConfiguration("publish_period_sec", default="1.0")

    # Optional RViz config (if you create one later)
    default_rviz = os.path.join(pkg_share, "rviz", "cartographer.rviz")
    rviz_config_file = LaunchConfiguration(
        "rviz_config",
        default=default_rviz,
    )

    # World + bridge + URDF paths
    world_file = LaunchConfiguration(
        "world",
        default=os.path.join(pkg_share, "worlds", "house.world"),
    )
    bridge_yaml = LaunchConfiguration(
        "bridge_yaml",
        default=os.path.join(pkg_share, "params", "tb3_bridge.yaml"),
    )
    urdf_file = LaunchConfiguration(
        "urdf",
        default=os.path.join(pkg_share, "urdf", "turtlebot3_waffle_pi.urdf"),
    )

    # -----------------------------
    # Gazebo resource path
    # -----------------------------
    pkg_models_path = os.path.join(pkg_share, "models")
    pkg_worlds_path = os.path.join(pkg_share, "worlds")
    existing_gz_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    combined_gz_path = ":".join([p for p in [pkg_models_path, pkg_worlds_path, existing_gz_path] if p])

    set_gz_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=combined_gz_path,
    )

    # -----------------------------
    # Gazebo Sim launch
    # -----------------------------
    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": ["-r ", world_file]
        }.items(),
    )

    # -----------------------------
    # ros_gz_bridge
    # -----------------------------
    bridge_node = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "--ros-args",
            "-p",
            ["config_file:=", bridge_yaml],
        ],
        parameters=[{"use_sim_time": use_sim_time}],
        output="screen",
    )

    # -----------------------------
    # robot_state_publisher
    # -----------------------------
    with open(os.path.join(pkg_share, "urdf", "turtlebot3_waffle_pi.urdf"), "r") as f:
        robot_description = f.read()

    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{
            "use_sim_time": use_sim_time,
            "robot_description": robot_description,
        }],
    )

    # -----------------------------
    # Cartographer
    # -----------------------------
    cartographer_node = Node(
        package="cartographer_ros",
        executable="cartographer_node",
        name="cartographer_node",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        arguments=[
            "-configuration_directory", cartographer_config_dir,
            "-configuration_basename", configuration_basename,
        ],
        remappings=[("scan", "/scan")],
    )

    occupancy_grid_node = Node(
        package="cartographer_ros",
        executable="cartographer_occupancy_grid_node",
        name="cartographer_occupancy_grid_node",
        parameters=[{
            "use_sim_time": use_sim_time,
            "resolution": resolution,
            "publish_period_sec": publish_period_sec,
        }],
        output="screen",
    )

    # -----------------------------
    # RViz (optional)
    # -----------------------------
    rviz_args = ["-d", default_rviz] if os.path.exists(default_rviz) else []
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=rviz_args,
        parameters=[{"use_sim_time": use_sim_time}],
        condition=IfCondition(use_rviz),
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
        DeclareLaunchArgument("use_sim_time", default_value=use_sim_time),
        DeclareLaunchArgument("use_rviz", default_value=use_rviz),
        DeclareLaunchArgument("cartographer_config_dir", default_value=cartographer_config_dir),
        DeclareLaunchArgument("configuration_basename", default_value=configuration_basename),
        DeclareLaunchArgument("resolution", default_value=resolution),
        DeclareLaunchArgument("publish_period_sec", default_value=publish_period_sec),
        DeclareLaunchArgument("rviz_config", default_value=rviz_config_file),
        DeclareLaunchArgument("world", default_value=world_file),
        DeclareLaunchArgument("bridge_yaml", default_value=bridge_yaml),
        DeclareLaunchArgument("urdf", default_value=urdf_file),

        set_gz_resource_path,
        gz_launch,
        bridge_node,
        rsp_node,
        cartographer_node,
        occupancy_grid_node,
        rviz_node,
        yolo_process,
    ])