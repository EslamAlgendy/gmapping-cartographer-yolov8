# Public distribution scope review — V8 (2026-10-11)

This curated archive was created specifically to avoid distributing optional or unverified *copies* of certain upstream materials. It remains a **release candidate**: human verification of provenance and license notices remains the depositor's responsibility. No legal or upstream ownership determination is made here.

## What changed relative to V7 DUAL_LICENSE_REVIEW

Removed archived copies of:

- `simulation/turtlebot3_gazebo/` (upstream/alternate world and launcher, unrelated to the default successfully smoke-tested demo launcher).
- `config/turtlebot3_cartographer/` (nonessential upstream-looking RViz snapshot).
- `code/gmapping/tb3_gmapping_demo/worlds/small_house.world` (AWS small house world is external and never passed a ROS Jazzy robot mapping smoke test).
- `code/gmapping/tb3_gmapping_demo/launch/Cartographer_detect.launch.py` (unsupported `yolobot_description` / `yolobot_control` dependencies).
- `code/gmapping/tb3_gmapping_demo/params/nav2_params.yaml` (nonessential configuration of uncertain provenance).
- `code/turtlebot3/semantic_fusion/test/` (unneeded upstream Apache-2.0 boilerplate tests).

These files are *not required to interpret the archived original maps, trajectories, evaluation statistics, or the default two live launchers*. Their omission does **not** establish fully standalone Gazebo/ROS reproduction; external packages, assets, and model weights are still required.

## Third-party resources retained and notices

- The archived `code/gmapping/tb3_gmapping_demo/models/turtlebot3_waffle_pi/` and `.../urdf/turtlebot3_waffle_pi.urdf` are TurtleBot3-derived resources; treat them under the originating ROBOTIS TurtleBot3 / TurtleBot3 Simulations licensing **rather than MIT**. The public repositories state Apache 2.0: https://github.com/ROBOTIS-GIT/turtlebot3 and https://github.com/ROBOTIS-GIT/turtlebot3_simulations . The `model.config` credits Taehun Lim (ROBOTIS). See `LICENSES/Apache-2.0.txt`. Exact local SDF modification history was not independently traced; verify if any other authors' material has been added before final public release.
- Any source excerpts in `code/patches/` are against their respective upstream works; this archive does not grant rights over upstream code. Consult `docs/UPSTREAM_REVISIONS.txt` and the original upstream notices.
- Other project launch/configuration files are treated as authored by the depositor according to the depositor's explicit assertion, not independent copyright verification. `code/gmapping/tb3_gmapping_demo/worlds/house.world` references Gazebo models but does not physically redistribute their meshes/textures.
- Third-party ROS / Gazebo / EVO / YOLO modules are installed separately, not redistributed as complete packages. YOLO weights not included.

## Research data preservation

The **28 specifically licensed original data files** listed in `docs/DATA_FILES_CC_BY_4_0.tsv` were copied **byte-for-byte from V7**, with no numerical or mapping edits. Historical review material in `docs/` may mention excluded paths; interpret it as provenance/history only. This document and the updated `README.md` control the **V8 distribution scope**.

## Publication readiness and limitations

Publishing a transparently described *incomplete research archive* is distinct from promising a clean-room reproducible runnable system. That limitation must appear in the public Zenodo Description. The depositor should still manually inspect the retained 3rd-party SDF/URDF and project-authored file provenance and run a full install if advertising independent reproducibility. Do not represent V8 as entirely MIT; original code is MIT, original experimental data is CC BY 4.0, and ROBOTIS-derived materials remain under upstream licensing.
