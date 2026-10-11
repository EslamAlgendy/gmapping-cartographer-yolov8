# Sole-creator declaration and rights review (2026-10-11)

The depositor explicitly identified **Eslam Ibrahem Hamed** as the **only author/creator** for the proposed Zenodo record and stated that Eslam alone is responsible for original project code, including the `semantic_fusion` implementation. Accordingly, the deposit metadata names no additional creators.

This is a **user-provided assertion**, not independent copyright verification for every file. A Zenodo creator is not necessarily the copyright holder of every bundled source, patch, or model. The archive includes files with third-party origins or pre-existing maintainer attributions. Their original notices should not be removed without source verification.

## Concrete unresolved attribution issues

- `code/gmapping/tb3_gmapping_demo/package.xml` now identifies Eslam Ibrahem Hamed as maintainer with depositor-provided contact `eslam.hamed@must.edu.eg`. The former placeholder `eslamalgendy@todo.todo` was removed. This contact update does not decide licensing or third-party rights.
- `code/turtlebot3/semantic_fusion/package.xml` and `setup.py` now list **Eslam Ibrahem Hamed** with `eslam.hamed@must.edu.eg` as maintainer, following the depositor's explicit confirmation on 2026-10-11 that this package is his own work. The previous package maintainer name and contact were removed from these metadata fields. This user assertion does not supersede third-party notices or historical upstream copyrights elsewhere in the archive.
- Upstream `slam_gmapping` patch context, ROBOTIS TurtleBot3 materials, Gazebo worlds/models, and any Ultralytics/YOLO assets must be treated under their applicable third-party licenses. Weights are not bundled.
- On 2026-10-11 Eslam explicitly approved **MIT** for his original code. The root `LICENSE` and `docs/LICENSE_SCOPE_AND_THIRD_PARTY.md` now document that grant; it does not override external rights. The depositor has separately approved CC BY 4.0 for his original maps, TUM trajectories and EVO outputs, listed in `docs/DATA_FILES_CC_BY_4_0.tsv`; some embedded upstream third-party files remain subject to unresolved provenance review. The record is not yet cleared for public publication.

**No research measurements, maps, TUM trajectories or EVO numerical contents were modified to record this authorship information.**
