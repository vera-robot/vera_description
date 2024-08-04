cmake_minimum_required(VERSION 3.5)
project(vera_description)

find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)

install(
  DIRECTORY launch urdf rviz meshes config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
