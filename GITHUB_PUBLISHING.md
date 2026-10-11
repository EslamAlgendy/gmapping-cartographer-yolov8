# Publish this research archive on GitHub

**Published and citable source:** [Zenodo v1.0.0-rc1](https://doi.org/10.5281/zenodo.23297292)  
**All-versions DOI:** [10.5281/zenodo.23297291](https://doi.org/10.5281/zenodo.23297291)

This folder is derived from the deposited V8 curated ZIP: `GMapping_Cartographer_YOLOv8_V8_CURATED_PUBLIC_REVIEW.zip`. **All 111 original archive entries remain byte-for-byte unchanged.** Four GitHub-only metadata files were added: `CITATION.cff`, `.gitignore`, `.gitattributes`, and this guide. It does not add model weights, external Gazebo assets, or installable upstream code.

## GitHub using GitHub CLI (recommended on Ubuntu)

1. Install `git` and the official `gh` GitHub CLI if needed, then run `gh auth login` and choose `GitHub.com` / browser sign-in.
2. Extract the accompanying *GitHub_Ready* ZIP into a fresh directory; open a terminal **inside** the extracted folder, the one containing `README.md`, `LICENSE`, `code/`, `results/`, `docs/`, etc.
3. Create the initial commit and a new public repository (do not expose auth tokens):

```bash
# Set git author once if not already set; use your actual name/email
# git config --global user.name "Eslam Ibrahem Hamed"
# git config --global user.email "eslam.hamed@must.edu.eg"
git init -b main
git add .
git commit -m "Publish research software mirror of Zenodo 1.0.0-rc1"
gh repo create gmapping-cartographer-yolov8 --public --source=. --remote=origin --push
```

If the repository name is already taken in your account, choose a different name.

## Alternative: create an empty repository on the GitHub website

1. Go to https://github.com/new and set repository name `gmapping-cartographer-yolov8` and visibility `Public`.
2. **Do not** initialize the new repository with a README, LICENSE, or .gitignore; they already exist in this folder.
3. In a terminal within the extracted directory, run:

```bash
git init -b main
git add .
git commit -m "Publish research software mirror of Zenodo 1.0.0-rc1"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/gmapping-cartographer-yolov8.git
git push -u origin main
```

Change `YOUR_GITHUB_USERNAME` to your actual GitHub username. GitHub does not accept an account password for authenticated Git pushes over HTTPS; use `gh auth login`, a credential manager, or a suitable personal access token. Do not paste passwords or tokens into a chat.

## Recommended repository settings

- **Description:** `ROS 2 Jazzy SLAM simulation (GMapping, Cartographer) with optional YOLOv8n; occupancy maps, trajectories and EVO results. Zenodo DOI: 10.5281/zenodo.23297292`
- **Website:** `https://doi.org/10.5281/zenodo.23297292`
- **Topics:** `ros2`, `slam`, `gmapping`, `cartographer`, `yolov8`, `gazebo`, `turtlebot3`, `robotics`
- **Visibility:** Public.
- **Release tag:** `v1.0.0-rc1` (optional; create after the first push), linking back to the Zenodo archive.

## Limits and licenses

- Original author-owned code: MIT, `LICENSE`.
- 28 specifically inventoried research data files: CC BY 4.0, `docs/DATA_FILES_CC_BY_4_0.tsv`.
- ROBOTIS-derived model SDF/URDF and third-party snippets: their original upstream licenses; do not relabel as MIT.
- Results with some `.json` filenames are **ZIP-format EVO archives**, not plain JSON. Preserve these bytes.
- `small_house.world` and YOLO model weights are not included in the V8 archive. Full clean-room installation has **not** been demonstrated. The 4 local tests do not prove YOLO detections modify SLAM occupancy maps.
- See `README.md`, `docs/RELEASE_GATE.md`, `docs/PUBLIC_RELEASE_SCOPE_V8.md`, and `docs/LICENSE_SCOPE_AND_THIRD_PARTY.md` for details.

**Keep Zenodo as the immutable cited release**, with GitHub as an accessible, version-controlled mirror. When code changes, publish a new GitHub release and (if appropriate) a new Zenodo version, rather than replacing the cited ZIP silently.
