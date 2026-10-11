# V6 review: launch-portability changes (UNVALIDATED in live ROS)

This archive is a **review candidate**, not a fully reproduced research software release. Existing numeric results and input trajectories have not been modified.

## Changes made only in this release copy

1. `sim.launch.py` and `cartographer_sim.launch.py` now accept `enable_yolo:=true|false` while preserving the original `true` launch default. For controlled baseline comparisons **explicitly pass** `enable_yolo:=false`; for YOLO conditions explicitly pass `enable_yolo:=true`.
2. YOLO runs from a copied, unmodified `yolov8_ros2_node.py` installed under the package share `tools/` directory, instead of calling the original user's home directory or activating a hard-coded venv. Pass `yolo_python:=/absolute/path/to/python` and `yolo_weights:=/absolute/path/to/yolov8n.pt`. The interpreter must import `rclpy`, `cv_bridge`, and `ultralytics`.
3. `world`, `extra_models_path`, `bridge_yaml`, `urdf`, `rviz_config`, and YOLO settings are launch arguments. Gazebo's `GZ_SIM_RESOURCE_PATH` incorporates local package models, local worlds, `extra_models_path` and the existing environment.
4. `cartographer_sim.launch.py` uses scalar declared launch defaults (fixes the recursive-looking `LaunchConfig(...)` introspection values) and applies `rviz_config`/`urdf` as runtime settings.
5. `CMakeLists.txt` installs `maps`, `rviz`, and `tools`; package.xml lists dependencies already required by the two launch files. Original LICENSE/maintainer placeholders have **not** been filled in.
6. Added `small_house.world` to the ROS package worlds directory (byte-for-byte copy of the supplied simulation world) for world switching; **64 AWS model folders remain external** and need pinned provenance and permission review.
7. Unmodified original `sim.launch.py`, `cartographer_sim.launch.py`, and `CMakeLists.txt` are preserved in `docs/original_launch/` for scientific traceability.

## Intentionally NOT rewritten

- `Cartographer_detect.launch.py` still depends on unavailable `yolobot_description` / `yolobot_control`; it remains an **unvalidated legacy launch**. Do not claim it works from this release.
- `simulation/turtlebot3_gazebo/launch/house.launch.py` is a Gazebo Classic launcher and is not an endorsed Gazebo Harmonic command.
- No behavioral changes were made to the detector's code, Cartographer configuration, GMapping parameters, maps, trajectories, or EVO archives.

## Verification needed on the author workstation

```bash
# In a clean terminal, with ROS Jazzy sourced and rebuilt package overlay sourced:
ros2 launch tb3_gmapping_demo sim.launch.py --show-args
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py --show-args
# Next: verify baseline and YOLO variants in BOTH worlds, checking ROS topics/TF, map output, detections and simulator asset loads.
```

**Warning:** `--show-args` is not a runtime or scientific reproduction test. If runtime behavior diverges, review `docs/original_launch/` rather than altering experimental results.
