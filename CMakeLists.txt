cmake_minimum_required(VERSION 3.6)

#
# For more details, see docs/building.rst
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

  option(BUILD_VERBOSE "Build reporting additional information (e.g download progress, ...)" OFF)

  set(CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR "${CMAKE_BINARY_DIR}"
    CACHE PATH "Directory where to download archives"
    )

  message(STATUS "***************************************************")
  message(STATUS "Build CMake from source: ${BUILD_CMAKE_FROM_SOURCE}")
  message(STATUS "***************************************************")

  include(${CMAKE_CURRENT_SOURCE_DIR}/CMakeUrls.cmake)

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

  set(binary_archive "linux32_binary")
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    set(binary_archive "linux64_binary")
  endif()
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

  # Add an empty external project
  function(cpd_ExternalProject_Add_Empty proj depends)
    set(depends_args)
    if(NOT depends STREQUAL "")
      set(depends_args DEPENDS ${depends})
    endif()
    ExternalProject_add(${proj}
      SOURCE_DIR ${CMAKE_BINARY_DIR}/${proj}
      DOWNLOAD_COMMAND ""
      UPDATE_COMMAND ""
      CONFIGURE_COMMAND ""
      BUILD_COMMAND ""
      BUILD_IN_SOURCE 1
      INSTALL_COMMAND ""
      ${depends_args}
      )
  endfunction()

  # Note: To minimize confusion between variables defined by CMake and
  #       variables used in this project. The following convention applies:
  #         CMakeProject_xxx : Variables defined in this project
  #         CMAKE_xxx  : Variables set by CMake

  set(${PROJECT_NAME}_CMAKE_CACHE_ARG)

  set(ep_download_no_progress_args)
  set(ep_log_configure_build_args)
  if(NOT BUILD_VERBOSE)
    set(ep_download_no_progress_args
      DOWNLOAD_NO_PROGRESS 1
      )
    set(ep_log_configure_build_args
      LOG_CONFIGURE 1
      LOG_BUILD 1
      )
  endif()

  #
  # CMakeProject_SOURCE_DIR: Always expect the sources (needed for `sdist`)
  #
  if(NOT DEFINED CMakeProject_SOURCE_DIR)
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
      ${ep_download_no_progress_args}
      )
    message(STATUS "SuperBuild - CMakeProject-src-download")
    message(STATUS "SuperBuild - CMakeProject-src-download - URL: ${${src_archive}_url}")
  else()
    cpd_ExternalProject_Add_Empty(CMakeProject-src-download "")
    message(STATUS "SuperBuild - CMakeProject-src-download")
  endif()
  message(STATUS "SuperBuild - CMakeProject-src-download - CMakeProject_SOURCE_DIR: ${CMakeProject_SOURCE_DIR}")

  if(NOT EXISTS ${CMakeProject_SOURCE_DIR})
    message(FATAL_ERROR "CMakeProject_SOURCE_DIR variable is defined but corresponds to nonexistent directory")
  endif()

  list(APPEND ${PROJECT_NAME}_DEPENDS CMakeProject-src-download)

  if(BUILD_CMAKE_FROM_SOURCE)

    #
    # CMakeProject_BINARY_DIR
    #
    if(NOT DEFINED CMakeProject_BINARY_DIR)
      set(CMakeProject_BINARY_DIR ${CMAKE_BINARY_DIR}/CMakeProject-build)

      ExternalProject_add(CMakeProject-build
        SOURCE_DIR ${CMakeProject_SOURCE_DIR}
        BINARY_DIR ${CMakeProject_BINARY_DIR}
        DOWNLOAD_COMMAND ""
        UPDATE_COMMAND ""
        BUILD_ALWAYS 1
        CMAKE_CACHE_ARGS
          -DBUILD_CursesDialog:BOOL=OFF
          -DCMAKE_USE_OPENSSL:BOOL=ON
          -DBUILD_TESTING:BOOL=OFF
          -DCMake_INSTALL_DEPENDENCIES:BOOL=ON
          -DCMAKE_INSTALL_MESSAGE:STRING=NEVER
        USES_TERMINAL_CONFIGURE 1
        USES_TERMINAL_BUILD 1
        ${ep_log_configure_build_args}
        INSTALL_COMMAND ""
        DEPENDS
          CMakeProject-src-download
        )
    else()
      cpd_ExternalProject_Add_Empty(CMakeProject-build "CMakeProject-src-download")
    endif()
    message(STATUS "SuperBuild -   CMakeProject-build")
    message(STATUS "SuperBuild -   CMakeProject-build - CMakeProject_BINARY_DIR: ${CMakeProject_BINARY_DIR}")

    if(NOT EXISTS ${CMakeProject_BINARY_DIR})
      message(FATAL_ERROR "CMakeProject_BINARY_DIR variable is defined but corresponds to nonexistent directory")
    endif()

    list(APPEND ${PROJECT_NAME}_DEPENDS CMakeProject-build)
    list(APPEND ${PROJECT_NAME}_CMAKE_CACHE_ARG
      -DCMakeProject_BINARY_DIR:PATH=${CMakeProject_BINARY_DIR}
      )

  else()

    #
    # CMakeProject_BINARY_DISTRIBUTION_DIR
    #

    if(${binary_archive}_sha256 STREQUAL "NA")
      message(FATAL_ERROR "Pre-built archives not available for '${binary_archive}'. Consider setting BUILD_CMAKE_FROM_SOURCE to ON.")
    endif()

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
      ${ep_download_no_progress_args}
      )
    message(STATUS "SuperBuild - CMakeProject-binary-download")
    message(STATUS "SuperBuild - CMakeProject-binary-download - URL: ${${binary_archive}_url}")

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

  # This adds an "install" target in the top-level directory. The
  # target will simply include the install rules associated with the
  # inner build
  install(SCRIPT ${CMAKE_BINARY_DIR}/${PROJECT_NAME}-build/cmake_install.cmake)

else()

  #-----------------------------------------------------------------------------
  if(BUILD_CMAKE_FROM_SOURCE)

    # Install CMakeProject
    install(CODE "
message(STATUS \"Install CMake project\")
include\(\"${CMakeProject_BINARY_DIR}/cmake_install.cmake\")
")

  #-----------------------------------------------------------------------------
  else()

    set(CMAKE_INSTALL_MESSAGE "NEVER")

    # Install all files from binary distribution
    file(GLOB_RECURSE binary_distribution_files
      LIST_DIRECTORIES FALSE
      ${CMakeProject_BINARY_DISTRIBUTION_DIR}/*
      )
    foreach(file IN LISTS binary_distribution_files)
      get_filename_component(directory ${file} DIRECTORY)
      file(RELATIVE_PATH relative_directory ${CMakeProject_BINARY_DISTRIBUTION_DIR} ${directory})
      set(type FILES)
      if(relative_directory STREQUAL "bin")
        set(type PROGRAMS)
      endif()
      # Skip symlinks like "CMake.app/Contents/Frameworks/QtWidgets.framework/Versions/Current"
      if(IS_SYMLINK ${file})
        continue()
      endif()
      set(_permissions)
      get_filename_component(filename ${file} NAME)
      if(filename MATCHES "ccmake|cmake|cmake-gui|cpack|ctest")
        set(_permissions PERMISSIONS
          OWNER_READ OWNER_WRITE OWNER_EXECUTE
          GROUP_READ GROUP_EXECUTE
          WORLD_READ WORLD_EXECUTE
          )
      endif()
      install(${type} ${file} DESTINATION "${relative_directory}" ${_permissions})
    endforeach()
  endif()

endif()
