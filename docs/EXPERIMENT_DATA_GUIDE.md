# Available experiment data — confirmation still required

**Scope:** GMapping / Cartographer, each with and without YOLOv8. RTAB-Map was not performed and is not part of the project.

## Map pairs

- `code/gmapping/tb3_gmapping_demo/maps/gmapping_map.pgm` + `.yaml` — named GMapping baseline.
- `code/gmapping/tb3_gmapping_demo/maps/gmapping_yolov8_map.pgm` + `.yaml` — named GMapping with YOLOv8.
- `code/gmapping/tb3_gmapping_demo/maps/cartographer_map.pgm` + `.yaml` — named Cartographer baseline.
- `code/gmapping/tb3_gmapping_demo/maps/cartographer_yolo.pgm` + `.yaml` — named Cartographer with YOLOv8.
- `house_map.pgm` + `.yaml` and `results/maps/turtlebot3_navigation2/map.*` — retained auxiliary maps; their provenance/role requires confirmation.

## Metric archives and pose trajectories

| Named evaluation | APE archive | RPE archive | Ground-truth/estimated TUM trajectories |
|---|---|---|---|
| GMapping baseline | `ape_gmapping.json` | `rpe_gmapping.json` | `gt_tum.txt` / `slam_tum.txt` — association to confirm |
| GMapping + YOLOv8 | `ape_gmapping_yolo.zip` (recomputed) | `rpe_gmapping_yolo.zip` (recomputed) | `gt_yolo_tum.txt` / `slam_yolo_tum.txt` — association to confirm |
| Cartographer baseline | `ape_cartographer.json` | `rpe_cartographer.json` | `gt_cartographer_tum.txt` / `slam_cartographer_tum.txt` |
| Cartographer + YOLOv8 | `ape_cartographer_yolo.json` | `rpe_cartographer_yolo.json` | `gt_cartographer_yolo_tum.txt` / `slam_cartographer_yolo_tum.txt` |

**Important format warning:** Files with names `ape_*.json` and `rpe_*.json` are ZIP-format containers (starting with `PK`), apparently saved evo result archives; do not feed them directly to `json.load`. Their filenames are left unchanged for traceability. Confirm with evo on the original evaluation environment before renaming/repackaging.

## Required before interpreting or replicating metrics

- Verify each trajectory-to-condition mapping, coordinate frames, scales and timestamps.
- Record exact `evo_ape` / `evo_rpe` CLI calls, including alignment, pose relation, delta, and unit settings.
- GMapping+YOLOv8 APE/RPE archives were recomputed from stored TUM trajectories, not recovered from the original output. Do not imply that the presence of YOLOv8 necessarily improved localization accuracy.
- Raw recorded sensor inputs (ROS bags) are not available; these data support analysis of the retained maps and trajectories, not full replay of the original runs.

**Recomputation:** See `docs/RESULTS_RECOMPUTATION.md` for exact evo commands.
