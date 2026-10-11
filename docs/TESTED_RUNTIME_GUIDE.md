# Build and launch guide — tested smoke tests vs pending clean-room work

## Build only the packaged custom demo (not entire upstream SLAM)

Set `ARCHIVE_DIR` to where you **extracted the ZIP**. In a ROS Jazzy shell:

```bash
export ARCHIVE_DIR=/absolute/path/to/extracted/zip
mkdir -p "$HOME/zenodo_test_ws/src"
cp -a "$ARCHIVE_DIR/code/gmapping/tb3_gmapping_demo" "$HOME/zenodo_test_ws/src/"
source /opt/ros/jazzy/setup.bash
cd "$HOME/zenodo_test_ws"
colcon build --symlink-install --packages-select tb3_gmapping_demo
source install/local_setup.bash
ros2 launch tb3_gmapping_demo sim.launch.py --show-args
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py --show-args
```

`colcon build`/`--show-args` verified on the researcher's independent *demo-package* workspace. **Runtime** depended on the earlier upstream `slam_gmapping` overlay. Check external dependencies with `ros2 pkg prefix slam_gmapping`, `ros2 pkg prefix cartographer_ros`, `ros2 pkg prefix ros_gz_bridge`. Full upstream build + patch not verified with this ZIP. See `docs/UPSTREAM_REVISIONS.txt`.

## One simulation at a time

Before running a new experiment, stop the previous launch via Ctrl+C and inspect lingering processes:

```bash
ps -eo pid,ppid,etimes,args | grep -E '[g]z sim|[g]z-sim|[r]os2 launch|[c]artographer_node'
```

Multiple active Gazebo servers previously caused odometry/TF time regression and Cartographer abort. Do not terminate unrelated users' processes.

## YOLO model and compatibility

The exact `yolov8n.pt` binary was NOT bundled. Supply an appropriately sourced/licensed model. Recorded expected SHA256:

`f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`

Set `YOLOPY` to an interpreter that imports ROS (`rclpy`, `cv_bridge`) plus ultralytics, and `WEIGHTS` to an absolute file path. Then follow `docs/NUMPY_CVBRIDGE_FIX.md` in the launch shell to activate the tested NumPy1 overlay.

```bash
export WEIGHTS=/absolute/path/to/yolov8n.pt
sha256sum "$WEIGHTS"
```

## Four scenarios (launch each separately, with no prior Gazebo instance)

```bash
# GMapping baseline
ros2 launch tb3_gmapping_demo sim.launch.py enable_yolo:=false use_rviz:=false
# Cartographer baseline
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py enable_yolo:=false use_rviz:=false
# GMapping + YOLOv8 (activate NumPy1 PYTHONPATH first)
ros2 launch tb3_gmapping_demo sim.launch.py enable_yolo:=true use_rviz:=false yolo_python:="$YOLOPY" yolo_weights:="$WEIGHTS"
# Cartographer + YOLOv8 (activate NumPy1 PYTHONPATH first)
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py enable_yolo:=true use_rviz:=false yolo_python:="$YOLOPY" yolo_weights:="$WEIGHTS"
```

The original local tests sourced `/opt/ros/jazzy/setup.bash`, `~/gmapping_ws/install/local_setup.bash`, then `~/zenodo_v6_test_ws/install/local_setup.bash`. This path is an *illustration of an existing overlay*, **not** a clean-room requirement for others. Use `bash scripts/preflight.sh` to identify missing runtime packages.

## Verify real messages, not just node names

From another ROS Jazzy terminal in the same ROS_DOMAIN_ID, while one mode runs, execute:

```bash
python3 "$ARCHIVE_DIR/scripts/validate_runtime.py" --algorithm gmapping
python3 "$ARCHIVE_DIR/scripts/validate_runtime.py" --algorithm cartographer
python3 "$ARCHIVE_DIR/scripts/validate_runtime.py" --algorithm gmapping --with-yolo
python3 "$ARCHIVE_DIR/scripts/validate_runtime.py" --algorithm cartographer --with-yolo
```

The validator is **new and not field-tested**; it checks a nonempty OccupancyGrid, publishers, and expected YOLO output. A `no_detections` message proves text output but is *not positive object detection*. Do not run all four validation commands on one active scenario.

## Other world

`house.world` is the default world used for smoke testing. `small_house.world` was not runtime-validated; it needs 64 AWS external models and a robot spawn mechanism. The archived world alone does not include a robot. See `docs/SMALL_HOUSE_LIMITATIONS.md` and `docs/THIRD_PARTY_ASSETS.md`.


**V8 scope note:** The previous optional `small_house.world` and unsupported `Cartographer_detect.launch.py` are deliberately not distributed. Follow `docs/PUBLIC_RELEASE_SCOPE_V8.md` and obtain optional worlds from the original upstream source if needed.
