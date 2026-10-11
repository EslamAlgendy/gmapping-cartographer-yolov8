# External Gazebo/AWS models and other upstream assets

The earlier V7 review contained an AWS-oriented `small_house.world` file listing approximately 64 named `model://aws_robomaker_residential_*` resources. **V8 omits this world file** and does not include its meshes or textures. See `docs/SMALL_HOUSE_LIMITATIONS.md`.

Upstream reference: https://github.com/aws-robotics/aws-robomaker-small-house-world . The repository is archived and was not independently rebuilt for ROS 2 Jazzy Gazebo Sim 8 in this release. Fetch from the rightful upstream source, check the relevant version/branch and licenses, and resolve model paths before any new tests.

**Retained ROBOTIS turtlebot3_waffle_pi resource copies** are third-party derivatives with their original model.config author credit and an Apache-2.0 notice in `LICENSES/Apache-2.0.txt`; do not treat them as Eslam's own MIT work. See `docs/PUBLIC_RELEASE_SCOPE_V8.md`.

Pretrained YOLO weights are not included. `house.world` may refer to external Gazebo assets but does not contain the external mesh/textures themselves.
