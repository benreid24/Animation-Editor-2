cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Fix behavior of CMAKE_CXX_STANDARD when targeting macOS.
if (POLICY CMP0025)
  cmake_policy(SET CMP0025 NEW)
endif()

project(Previewer C CXX)

# BLIB will inherit these settings as well
option(STATIC_LINK "On to link statically" On)
option(BUILD_TESTS "On to build unit tests" Off)
option(BUILD_EXAMPLES "On to build examples" Off)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_INSTALL_PREFIX .)

add_subdirectory(lib/BLIB)
include_directories(lib/BLIB/include)
include_directories(lib/BLIB/lib/SFML/include)

add_executable(Previewer)
target_sources(Previewer PUBLIC main.cpp)

if (MSVC)
    # warning level 4 and all warnings as errors
    target_compile_options(Previewer PUBLIC /W4 /WX)
else()
    # lots of warnings and all warnings as errors
    target_compile_options(Previewer PUBLIC -Wall -Wextra -pedantic)
endif()

if (STATIC_LINK)
    if (WIN32)
        SET(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
        set(BUILD_SHARED_LIBRARIES OFF)
        set(CMAKE_EXE_LINKER_FLAGS "-static -static-libgcc -static-libstdc++")
    endif()
endif()

target_link_libraries(Previewer PRIVATE
    BLIB

    sfml-graphics
    sfml-window
    sfml-network
    sfml-audio
    sfml-system
)

set_target_properties(Previewer
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    OUTPUT_NAME "Previewer"
)
