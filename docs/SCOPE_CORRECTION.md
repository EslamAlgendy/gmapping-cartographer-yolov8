# Scope correction from V3 review

The author explicitly confirmed that the experiments used **GMapping** and **Cartographer** with **YOLOv8**, and that **RTAB-Map was not used**.

Changes to this V4 REVIEW package:

- Removed the entire `code/turtlebot3/turtlebot3_rtab/` subtree.
- Corrected README, data guide and release validation/checklist to reflect GMapping/Cartographer only.
- Preserved original source code, model/world assets already present in the V3 archive, metrics, trajectories, and their byte contents elsewhere in the ZIP.
- Clarified that `ape_*.json` and `rpe_*.json` are ZIP-format result archives, not plain JSON, and that no GMapping+YOLOv8 APE/RPE archives are included.
- Removed old embedded archive-hash note; an external SHA256 file accompanies the ZIP.

This does not establish that all four configurations build or run. V4 remains a **REVIEW** archive pending validation and license checks.

## V5 update

The missing GMapping+YOLOv8 EVO archives were **recomputed from retained TUM trajectories** and added to a later review release; the sentence above about their absence applies only to V4.
