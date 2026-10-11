# GMapping + YOLOv8: recomputed EVO results (REVIEW)

The originally saved GMapping+YOLOv8 EVO APE/RPE archives were not found during the local search. Their original input trajectories **were retained**, and these two results were calculated on 2026-10-11 from those files, not recovered from the original experiment. No sensor bags were retained.

Input trajectories (already included at `results/metrics/`):
- `gt_yolo_tum.txt` (ground truth)
- `slam_yolo_tum.txt` (estimated)

Author-recorded recomputation commands (run from the directory containing the trajectories):

```bash
evo_ape tum gt_yolo_tum.txt slam_yolo_tum.txt -a -r full \
  --save_results ape_gmapping_yolo.zip

evo_rpe tum gt_yolo_tum.txt slam_yolo_tum.txt \
  --delta 1 --delta_unit m --all_pairs -a -r full \
  --save_results rpe_gmapping_yolo.zip
```

EVO version reported in the author environment: `1.34.3`.

| Measure | RMSE | Settings |
|---|---:|---|
| APE | 1.903667 | full transformation, SE(3) Umeyama alignment |
| RPE | 0.255551 | full transformation, delta=1 m, all pairs, SE(3) alignment |

The evo output identifies **full transformation error as unit-less**. Do not label these RMSE values as meters. Confirm identical evaluation conditions, reference frames, timestamp alignment and trajectory comparability before making causal or quantitative superiority claims across runs.

All earlier `ape_*.json` and `rpe_*.json` files in the V4 archive are **ZIP-format evo result archives despite their `.json` filenames**. They have been preserved byte-for-byte for provenance; use a ZIP reader/evo rather than JSON decoding.

**Release remains blocked:** unverified external Gazebo/YOLO dependencies, third-party source provenance/rights, lingering portability questions, and clean-environment testing. This package is not ready to publish on Zenodo yet.
