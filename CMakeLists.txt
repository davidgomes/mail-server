project (mail_server)
cmake_minimum_required (VERSION 2.8)

set (CMAKE_CXX_FLAGS "-Wall")

file (GLOB_RECURSE PROJECT_SOURCES "src/*.cpp")

include_directories (include)
add_executable (mail-server ${PROJECT_SOURCES})
