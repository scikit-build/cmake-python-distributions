cmake_minimum_required(VERSION 3.6)

#
# This project has been designed to work with scikit-build.
#
# It allows to create both source and binary distributions of
# CMake.
#
# This is done ensuring source files and build artifacts
# are copied and/or generated in expected locations.
#
# Source distribution (sdist)
# ---------------------------
#
# CMake sources will always be downloaded in the ``<ROOT>/src``
# directory.
#
# This will ensure that the rules specified in ``<ROOT>/MANIFEST.in``
# can successfully glob the source files.
#
# The source distribution is generated using the following
# command::
#
#   python setup.pt sdist
#
#
# Binary distribution (build, bdist, bdist_wheel)
# -----------------------------------------------
#
# The project has two mode of operations:
#
#  1. build CMake from source  (BUILD_CMAKE_FROM_SOURCE set to ON)
#  2. download CMake binaries  (BUILD_CMAKE_FROM_SOURCE set to OFF)
#
#
# Depending on the platform, option ``BUILD_CMAKE_FROM_SOURCE`` has
# different default:
#
#   - Linux: ON
#   - MacOSX: OFF
#   - Windows: OFF
#
# The binary distribution is generated using the following
# command::
#
#   python setup.pt bdist_wheel
#
#
# Changing the default mode is achieved by explicitly passing the option
# to CMake::
#
#   python setup.pt bdist_wheel -- -DBUILD_CMAKE_FROM_SOURCE:BOOL=ON
#
#
# Optimizations
# -------------
#
# On a given platform, when building different "flavor" of CMake python wheels (one
# for each <python tag>-<abi tag>), the whole process can be made faster by avoiding
# to re-download CMake.
#
# By passing the option ``-DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/path/to/cache``,
# successive build will re-use existing archives instead of re-downloading them.
#

project(CMakePythonDistributions NONE)

if(NOT DEFINED CMakePythonDistributions_SUPERBUILD)
  set(CMakePythonDistributions_SUPERBUILD 1)
endif()

if(CMakePythonDistributions_SUPERBUILD)

  enable_language(CXX)

  #-----------------------------------------------------------------------------
  # Options
  set(default ON)
  if(WIN32 OR APPLE)
    set(default OFF)
  endif()
  option(BUILD_CMAKE_FROM_SOURCE "Build CMake from source" ${default})

  set(CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR "${CMAKE_BINARY_DIR}"
    CACHE PATH "Directory where to download archives"
    )

  message(STATUS "***************************************************")
  message(STATUS "Build CMake from source: ${BUILD_CMAKE_FROM_SOURCE}")
  message(STATUS "***************************************************")

  #-----------------------------------------------------------------------------
  # CMake sources
  set(unix_source_url       "https://cmake.org/files/v3.6/cmake-3.6.2.tar.gz")
  set(unix_source_sha256    "189ae32a6ac398bb2f523ae77f70d463a6549926cde1544cd9cc7c6609f8b346")

  set(windows_source_url    "https://cmake.org/files/v3.6/cmake-3.6.2.zip")
  set(windows_source_sha256 "ccf93db0527c35676ab74319bb3ef1ef4f5149d3b09aab1a58559143c1f4f673")

  #-----------------------------------------------------------------------------
  # CMake binaries
  set(linux_binary_url    "https://cmake.org/files/v3.6/cmake-3.6.2-Linux-x86_64.tar.gz")
  set(linux_binary_sha256 "5df4b69d9e85093ae78b1070d5cb9f824ce0bdd02528948c3f6a740e240083e5")

  set(macosx_binary_url    "https://cmake.org/files/v3.6/cmake-3.6.2-Darwin-x86_64.tar.gz")
  set(macosx_binary_sha256 "e3ac82120298095245c9948eb11ddfb4b552f5f056ce0ec3c82e3f3a15c53752")

  set(win32_binary_url    "https://cmake.org/files/v3.6/cmake-3.6.2-win32-x86.zip")
  set(win32_binary_sha256 "613eec5a8b2e2c49826e0e8e18f516b6f2b481309ae55925d226ce8ab78b0fba")

  set(win64_binary_url    "https://cmake.org/files/v3.6/cmake-3.6.2-win64-x64.zip")
  set(win64_binary_sha256 "61337a0528fc3902d7f2f7594959aa6aa48a52863dd2da335a0e248b5eb8acaf")

  #-----------------------------------------------------------------------------
  # Which archives ?

  function(check_archive_var archive_var)
    if(NOT DEFINED "${archive_var}_url")
      message(FATAL_ERROR "Failed to determine which archive to download: '${archive_var}_url' variable is not defined")
    endif()
    if(NOT DEFINED "${archive_var}_sha256")
      message(FATAL_ERROR "Could you make sure variable '${archive_var}_sha256' is defined ?")
    endif()
  endfunction()

  set(src_archive "unix_source")
  if(WIN32)
    set(src_archive "windows_source")
  endif()
  check_archive_var("${src_archive}")

  set(binary_archive "linux_binary")
  if(APPLE)
    set(binary_archive "macosx_binary")
  endif()
  if(WIN32)
    set(binary_archive "win32_binary")
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
      set(binary_archive "win64_binary")
    endif()
  endif()
  check_archive_var("${binary_archive}")

  #-----------------------------------------------------------------------------
  include(ExternalProject)

  # Note: To minimize confusion between variables defined by CMake and
  #       variables used in this project. The following convention applies:
  #         CMakeProject_xxx : Variables defined in this project
  #         CMAKE_xxx  : Variables set by CMake

  set(CMakeProject_SOURCE_DIR "${CMAKE_SOURCE_DIR}/src")

  # Download selected source archive
  ExternalProject_add(CMakeProject-src-download
    SOURCE_DIR ${CMakeProject_SOURCE_DIR}
    URL ${${src_archive}_url}
    URL_HASH SHA256=${${src_archive}_sha256}
    DOWNLOAD_DIR ${CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR}
    USES_TERMINAL_DOWNLOAD 1
    CONFIGURE_COMMAND ""
    BUILD_COMMAND ""
    BUILD_IN_SOURCE 1
    INSTALL_COMMAND ""
    )
  message(STATUS "SuperBuild - CMakeProject-src-download")

  set(${PROJECT_NAME}_DEPENDS CMakeProject-src-download)
  set(${PROJECT_NAME}_CMAKE_CACHE_ARG)

  if(BUILD_CMAKE_FROM_SOURCE)

    set(CMakeProject_BINARY_DIR ${CMAKE_BINARY_DIR}/CMakeProject-build)

    ExternalProject_add(CMakeProject-build
      SOURCE_DIR ${CMakeProject_SOURCE_DIR}
      BINARY_DIR ${CMakeProject_BINARY_DIR}
      DOWNLOAD_COMMAND ""
      UPDATE_COMMAND ""
      CMAKE_CACHE_ARGS
        -DBUILD_CursesDialog:BOOL=OFF
        -DCMAKE_USE_OPENSSL:BOOL=ON
        -DBUILD_TESTING:BOOL=OFF
        -DCMake_INSTALL_DEPENDENCIES:BOOL=ON
      USES_TERMINAL_CONFIGURE 1
      USES_TERMINAL_BUILD 1
      INSTALL_COMMAND ""
      DEPENDS
        CMakeProject-src-download
      )
    message(STATUS "SuperBuild -   CMakeProject-build")

    list(APPEND ${PROJECT_NAME}_DEPENDS CMakeProject-build)
    list(APPEND ${PROJECT_NAME}_CMAKE_CACHE_ARG
      -DCMakeProject_BINARY_DIR:PATH=${CMakeProject_BINARY_DIR}
      )

  else()

    set(CMakeProject_BINARY_DISTRIBUTION_DIR "${CMAKE_BINARY_DIR}/CMakeProject-binary-distribution")

    # Download selected binary archive
    ExternalProject_add(CMakeProject-binary-download
      SOURCE_DIR ${CMakeProject_BINARY_DISTRIBUTION_DIR}
      URL ${${binary_archive}_url}
      URL_HASH SHA256=${${binary_archive}_sha256}
      DOWNLOAD_DIR ${CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR}
      USES_TERMINAL_DOWNLOAD 1
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND ""
      )
    message(STATUS "SuperBuild - CMakeProject-binary-download")

    list(APPEND ${PROJECT_NAME}_DEPENDS CMakeProject-binary-download)
    list(APPEND ${PROJECT_NAME}_CMAKE_CACHE_ARG
      -DCMakeProject_BINARY_DISTRIBUTION_DIR:PATH=${CMakeProject_BINARY_DISTRIBUTION_DIR}
      )

  endif()

  ExternalProject_add(${PROJECT_NAME}
    SOURCE_DIR ${CMAKE_SOURCE_DIR}
    BINARY_DIR ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_CACHE_ARGS
      -D${PROJECT_NAME}_SUPERBUILD:BOOL=0
      -DBUILD_CMAKE_FROM_SOURCE:BOOL=${BUILD_CMAKE_FROM_SOURCE}
      -DCMAKE_INSTALL_PREFIX:PATH=${CMAKE_INSTALL_PREFIX}
      ${${PROJECT_NAME}_CMAKE_CACHE_ARG}
    USES_TERMINAL_CONFIGURE 1
    INSTALL_COMMAND ""
    DEPENDS
      ${${PROJECT_NAME}_DEPENDS}
    )
  message(STATUS "SuperBuild -   ${PROJECT_NAME}")

  install(SCRIPT ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build/cmake_install.cmake)

else()

  #-----------------------------------------------------------------------------
  if(BUILD_CMAKE_FROM_SOURCE)

    # Install CMakeProject
    install(CODE "
include\(\"${CMakeProject_BINARY_DIR}/cmake_install.cmake\")
")

  #-----------------------------------------------------------------------------
  else()

    # Install all files from binary distribution
    file(GLOB_RECURSE binary_distribution_files
      LIST_DIRECTORIES FALSE
      ${CMakeProject_BINARY_DISTRIBUTION_DIR}/*
      )
    foreach(file IN LISTS binary_distribution_files)
      get_filename_component(directory ${file} DIRECTORY)
      file(RELATIVE_PATH relative_directory ${CMakeProject_BINARY_DISTRIBUTION_DIR} ${directory})
      install(FILES ${file} DESTINATION "${relative_directory}")
    endforeach()
  endif()

endif()
