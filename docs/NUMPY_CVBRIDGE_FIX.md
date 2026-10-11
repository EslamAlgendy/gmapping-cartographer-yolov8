# Jazzy / NumPy ABI compatibility — tested fix

Observed YOLO error: compiled NumPy 1.x `cv_bridge` cannot run with virtualenv NumPy 2.4.2; crash in `imgmsg_to_cv2` and exit -11. Camera ROS publisher used RELIABLE QoS and this was NOT a QoS mismatch.

Safe, tested approach (does **not** modify original YOLO venv):

```bash
source /opt/ros/jazzy/setup.bash
export YOLOPY="$HOME/gmapping_ws/yolo_venv/bin/python" # change for your setup
export COMPAT="$HOME/zenodo_v6_test_ws/yolo_numpy1_compat" # any writable test directory
mkdir -p "$COMPAT"
"$YOLOPY" -m pip install --no-deps --target "$COMPAT" 'numpy==1.26.4' 'opencv-python==4.11.0.86'
export PYTHONPATH="$COMPAT${PYTHONPATH:+:$PYTHONPATH}"
"$YOLOPY" -c 'import numpy, cv2, rclpy, ultralytics, cv_bridge; print(numpy.__version__, cv2.__version__)'
```

The author tested actual `CvBridge().imgmsg_to_cv2(msg, desired_encoding="bgr8")` conversion on a 10 x 10 RGB Image: `RESULT: PASS`. The compatible PYTHONPATH must be set **in the terminal running the launch**, so the YOLO subprocess inherits it. YOLO weight file and existing ultralytics/PyTorch/ROS Python dependencies remain necessary. This is an overlay workaround, **not** a validated fresh virtual environment. `dependencies/yolo_jazzy_compat_constraints.txt` records the precise tested pins.
