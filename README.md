# GMapping and Cartographer with YOLOv8 — ROS 2 software and research artifacts

**Curated public-review archive (V8, version 1.0.0-rc1).** Zenodo creator: **Eslam Ibrahem Hamed**. Contact: `eslam.hamed@must.edu.eg`.

## Contents and licensing

- **Original source code authored by Eslam Ibrahem Hamed**: MIT (`LICENSE`). This grant does not relicense third-party portions.
- **Original experimental occupancy-grid maps, TUM trajectories, and EVO evaluation archives**: CC BY 4.0 (`LICENSES/CC-BY-4.0.md` and `docs/DATA_FILES_CC_BY_4_0.tsv`, which identifies precisely 28 files).
- **Redistributed upstream ROBOTIS TurtleBot3 model/URDF resources, patches and any other third-party fragments**: original upstream conditions and attribution; see `LICENSES/Apache-2.0.txt`, `docs/LICENSE_SCOPE_AND_THIRD_PARTY.md`, `docs/PUBLIC_RELEASE_SCOPE_V8.md`. The MIT root license does not apply to third-party content.

Some third-party world/source snapshots and optional/unsupported files present in earlier *review* ZIPs were **removed** from this curated archive. See `docs/PUBLIC_RELEASE_SCOPE_V8.md` for an exact list. Pretrained YOLO weights and AWS house meshes/textures have never been bundled.

## Experiments and evidence

Four reported configurations: **GMapping**, **GMapping + YOLOv8n**, **Cartographer**, **Cartographer + YOLOv8n**. No RTAB-Map experiments are included.

ROS 2 Jazzy / Ubuntu 24.04 / Gazebo Sim 8 **local smoke-test observations**, on the researcher's machine with existing upstream overlays:

| Mode | Observed evidence | Limit |
|---|---|---|
| GMapping | 384 × 384 nonempty OccupancyGrid, 4,245 known cells | Controlled driving/loop-closure not verified |
| Cartographer | Submaps ~3.33 Hz; 168 × 155 nonempty grid, 5,622 known cells | Multiple stale Gazebo servers were cleaned before successful run |
| GMapping + YOLOv8n | Annotated camera images ~5.86 Hz, one GMapping map publisher | Concurrent map-content test not separately retained |
| Cartographer + YOLOv8n | Submaps ~3.33 Hz, annotations ~5.65 Hz, 138 × 112 nonempty map, 4,253 known cells | `no_detections` sample; no positive object detection proven |

**The tests do not demonstrate that YOLO detections directly alter or improve SLAM maps.** No clean-room reproduction was completed. Some EVO files with `.json` extensions are ZIP-format EVO archives; see `docs/RESULTS_RECOMPUTATION.md`. Two GMapping+YOLOv8 evaluation files were recomputed from retained TUM trajectories and are identified accordingly. These files must not be represented as originally saved results.

## How to use

1. Read `docs/TESTED_RUNTIME_GUIDE.md`, `docs/NUMPY_CVBRIDGE_FIX.md`, `docs/UPSTREAM_REVISIONS.txt` and `docs/PUBLIC_RELEASE_SCOPE_V8.md`.
2. Install the upstream ROS/Jazzy and robot-model dependencies under their own licenses. `slam_gmapping` source/patch full independent build remains unverified.
3. For a previous local four-mode smoke-test setup, the default world was **`house.world`**. The AWS-based `small_house.world` was not tested and is **not distributed** in this curated ZIP; obtain external resources from their rightful providers.
4. Verify `docs/FILE_MANIFEST_SHA256.tsv` with `python3 scripts/check_archive.py` after extracting.

This is a **documented research software release candidate**, not a turnkey, fully reproducible software environment. All third-party credits must be retained. For deposit details, see `metadata/ZENODO_DEPOSIT_DRAFT.md` and `docs/PUBLIC_RELEASE_SCOPE_V8.md`.
