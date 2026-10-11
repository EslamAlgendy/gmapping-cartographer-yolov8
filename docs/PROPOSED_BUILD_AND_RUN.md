# Proposed ROS 2 Jazzy build and smoke tests (not yet validated)

The source archive does not bundle `slam_gmapping` or the full TurtleBot3 and Gazebo dependency trees. Apply the provided GMapping patch to the **recorded upstream revision**, after reviewing the patch and the source license, then install remaining ROS/Jazzy prerequisites. `docs/UPSTREAM_REVISIONS.txt` has recorded hashes but public URLs and legal review remain open.

## Assemble test workspace (do not overwrite your original)

After extracting the archive to a directory named `$ARCHIVE`:

```bash
mkdir -p ~/zenodo_test_ws/src
cp -a "$ARCHIVE/code/gmapping/tb3_gmapping_demo" ~/zenodo_test_ws/src/
cp -a "$ARCHIVE/code/turtlebot3/semantic_fusion" ~/zenodo_test_ws/src/
# Add the pinned, patched upstream slam_gmapping repository under ~/zenodo_test_ws/src/
# Obtain the ROS/Gazebo dependencies from the documented upstream locations.
source /opt/ros/jazzy/setup.bash
cd ~/zenodo_test_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

**Do not execute a baseline/YOLO launch until you've verified the correct world assets, robot TF, and topic interfaces; build success is not proof of reproduction.**

## Configure detector interpreter and weights

The archived weights are NOT distributed. Use the author's model source/license after verification and check the expected SHA-256 hash `f59b3d833e2ff32e194b5bb8e08d211dc7c5bdf144b90d2c8412c47ccfc83b36`. Set `YOLOPY` to an interpreter with ROS Python bindings, `cv_bridge`, `ultralytics` and its transitive dependencies, and `WEIGHTS` to an absolute file path:

```bash
YOLOPY=/absolute/path/to/python
WEIGHTS=/absolute/path/to/yolov8n.pt
sha256sum "$WEIGHTS"
"$YOLOPY" -c 'import rclpy, cv_bridge, ultralytics; print("YOLO interpreter imports OK")'
```

## Four proposed launch variants (new **portability** launchers)

```bash
# GMapping baseline
ros2 launch tb3_gmapping_demo sim.launch.py enable_yolo:=false

# GMapping + YOLOv8
ros2 launch tb3_gmapping_demo sim.launch.py enable_yolo:=true yolo_python:="$YOLOPY" yolo_weights:="$WEIGHTS"

# Cartographer baseline
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py enable_yolo:=false

# Cartographer + YOLOv8
ros2 launch tb3_gmapping_demo cartographer_sim.launch.py enable_yolo:=true yolo_python:="$YOLOPY" yolo_weights:="$WEIGHTS"
```

To use `small_house.world` with any command, append:

```bash
world:="$(ros2 pkg prefix --share tb3_gmapping_demo)/worlds/small_house.world" extra_models_path:=/absolute/path/to/turtlebot3_gazebo/models
```

These launchers have not yet been run with Gazebo on the author's machine. `small_house.world` references 64 AWS residential model names; verify both direct and nested model/mesh/texture dependencies, rights, and correct `GZ_SIM_RESOURCE_PATH`. The included `house.world` also depends on external Gazebo Fuel model URIs. The separately packaged TurtleBot3 Gazebo `house.world` differs from the demo world.

## Output and limitations

All original maps, TUM trajectories, and saved EVO result archives remain unchanged. The two `GMapping + YOLOv8` metric archives are clearly marked as recomputed. The raw ROS sensor bags do not exist in this release, so the original sensor stream cannot be replayed. ROS 2 build, simulation, timestamps, TF frames, and eval flag equivalence must be verified before publishing or claiming reproduction.
