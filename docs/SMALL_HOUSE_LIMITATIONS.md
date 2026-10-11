# small_house.world — excluded from V8 public review ZIP

`small_house.world` was present in the older local V7 review package but removed in this curated V8 public review copy because its provenance/distribution path and Gazebo Sim 8/TurtleBot3 robot-spawn run were not verified. It referenced approximately 64 AWS RoboMaker residential model folders, whose meshes/textures are not included. The world itself did not spawn a robot.

Reference upstream: https://github.com/aws-robotics/aws-robomaker-small-house-world (archived repository). Its ROS-1/ROS-2 branches, assets and specific licenses need upstream review; do not imply the archived Jazzy test validated it. Retain research notes and model audit separately from any claims of functionality. The default `house.world` was tested in all four local cases.
