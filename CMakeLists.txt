project (mail_server)
cmake_minimum_required (VERSION 2.8)

set (CMAKE_CXX_FLAGS "-Wall")

file (GLOB_RECURSE CLIENT_SOURCES "src/client*.cpp")
file (GLOB_RECURSE SERVER_SOURCES "src/server*.cpp")

include_directories (include)
add_executable (mail-server ${SERVER_SOURCES})
add_executable (mail-client ${CLIENT_SOURCES})
