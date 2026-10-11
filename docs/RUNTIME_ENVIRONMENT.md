# Tested local environment (reported by experiment author)

| Component | Version |
|---|---|
| Operating system | Ubuntu 24.04.4 LTS |
| ROS 2 | Jazzy |
| Gazebo Sim | 8.10.0 (Harmonic) |
| System Python | 3.12.3 |
| NumPy (YOLO and evo venvs) | 2.4.2 |
| OpenCV Python (YOLO venv) | 4.13.0.92 |
| SciPy (YOLO and evo venvs) | 1.17.1 |
| PyTorch (YOLO venv) | 2.10.0 |
| Torchvision (YOLO venv) | 0.25.0 |
| Ultralytics (YOLO venv) | 8.4.18 |
| Ultralytics THOP (YOLO venv) | 2.0.18 |
| evo (evo venv) | 1.34.3 |
| Matplotlib (evo venv) | 3.10.8 |

The accompanying `dependencies/*_requirements.txt` files record pinned packages
found in the existing local environments, **not** a minimal dependency specification.
CUDA/cuDNN versions, GPU and driver versions, system apt packages, and some ROS
package versions have not yet been captured or validated.

Exact upstream Git commit identifiers for TurtleBot3, its simulation/messages
and slam_gmapping are in `docs/UPSTREAM_REVISIONS.txt`. Those local Git branches
must not be replaced casually by a newer upstream version.
