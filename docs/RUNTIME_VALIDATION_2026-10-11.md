# Field smoke-test evidence, 2026-10-11

**Source:** researcher-submitted console outputs from ROS 2 Jazzy / Gazebo Sim 8; not a ROS bag or complete raw log. V6 launchers were sourced after the author's original `gmapping_ws` build, so this was not standalone reproduction.

| Scenario | Result | Details |
|---|---|---|
| GMapping baseline | MAP PASS | `/slam_gmapping` one node, `/map` one publisher, LiDAR ~15 Hz; `map`, 384x384, 0.05 m/cell, 147,456 total, 4,245 known, 313 occupied |
| Cartographer baseline | MAP PASS | `/cartographer_node`, `/cartographer_occupancy_grid_node`; submaps ~3.333 Hz; map 168x155, 0.05 m/cell, 5,622 known, 476 occupied |
| GMapping + YOLOv8 | CO-RUNTIME PASS | YOLO annotated stream ~5.865 Hz, camera pub/sub RELIABLE, one GMapping map publisher. Did not separately subscribe to map data concurrently. |
| Cartographer + YOLOv8 | MAP + CO-RUNTIME PASS | submaps ~3.333 Hz, annotations ~5.648 Hz, map 138x112, 0.05 m/cell, 4,253 known, 244 occupied; detection example `no_detections` |

### Incident: old Gazebo servers caused time regression

Cartographer initially stopped with exit code -6 and `PoseExtrapolator::AddOdometryData()` fatal invariant on old odometry time; LaserScan timestamps were observed jumping backward by ~713 seconds and TF_OLD_DATA warnings appeared. Inspection found **three** lingering `gz sim server` plus GUI processes. After the old Gazebo processes were closed and a single simulation was started, Cartographer published 3.33 Hz submaps and an actual map. This supports stale/conflicting simulation time as the source but is not a controlled root-cause experiment. Running just one world at a time is essential.

### Incident: cv_bridge incompatible with NumPy 2

YOLO VENV: NumPy 2.4.2, OpenCV 4.13.0.92. System: NumPy 1.26.4. `cv_bridge.imgmsg_to_cv2()` hit a NumPy 1.x ABI incompatibility and YOLO exited -11. Installing NumPy **1.26.4** + OpenCV **4.11.0.86** into a separate `pip --target` directory and prepending it to PYTHONPATH gave a `CvBridge` RGB→BGR conversion PASS and subsequent YOLO image stream. See `docs/NUMPY_CVBRIDGE_FIX.md`.

### Evidence limitations

No positive object detection was documented: the sampled `/yolo/detections_text` was `no_detections` for class filter 0,56,60 and confidence 0.35. No proof that YOLO modifies SLAM estimation; no raw ROS bags; no controlled mapping-with-motion check; no tested small_house world; no clean-room fresh install. These smoke-test map dimensions and image rates are NOT experimental performance comparisons.
