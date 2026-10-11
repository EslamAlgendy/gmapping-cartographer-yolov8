#!/usr/bin/env bash
# Non-destructive inspection; never kill other processes.
set -u
printf 'ROS_DISTRO=%s
' "${ROS_DISTRO:-unset}"
for package in tb3_gmapping_demo slam_gmapping cartographer_ros ros_gz_sim ros_gz_bridge robot_state_publisher; do
  if command -v ros2 >/dev/null && ros2 pkg prefix "$package" >/dev/null 2>&1; then
    echo "OK $package: $(ros2 pkg prefix "$package")"
  else
    echo "MISSING $package"
  fi
done
echo 'Potential stale Gazebo/ROS launches:'
ps -eo pid,ppid,etimes,args | grep -E '[g]z sim|[g]z-sim|[r]os2 launch|[c]artographer_node' || true
if [ -n "${YOLOPY:-}" ] && [ -x "${YOLOPY}" ]; then
  "$YOLOPY" -c 'import numpy,cv2; print("numpy",numpy.__version__,"opencv",cv2.__version__)' || true
fi
if [ -n "${WEIGHTS:-}" ] && [ -f "${WEIGHTS}" ]; then sha256sum "$WEIGHTS"; fi
