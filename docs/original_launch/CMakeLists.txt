cmake_minimum_required(VERSION 3.8)
project(tb3_gmapping_demo)

find_package(ament_cmake REQUIRED)

# Install folders (launch files, worlds, models, params, urdf)
install(DIRECTORY
  launch
  config
  worlds
  models
  params
  urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()