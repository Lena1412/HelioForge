cmake_minimum_required(VERSION 3.20)
project(helioforge_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(helioforge_native
    src/helioforge_native/kepler.cpp
)

if (MSVC)
    target_compile_options(helioforge_native PRIVATE /W4)
else()
    target_compile_options(helioforge_native PRIVATE -Wall -Wextra -Wpedantic)
endif()

install(TARGETS helioforge_native
    LIBRARY DESTINATION .
    RUNTIME DESTINATION .
    ARCHIVE DESTINATION .
)
