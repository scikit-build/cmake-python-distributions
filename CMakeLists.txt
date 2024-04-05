cmake_minimum_required(VERSION 3.6)

#
# For more details, see docs/building.rst
#

project(CMakePythonDistributions NONE)

# Set a default build type if none was specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  message(STATUS "Setting build type to 'Release' as none was specified.")
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
  mark_as_advanced(CMAKE_BUILD_TYPE)
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

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

  option(BUILD_VERBOSE "Build reporting additional information (e.g download progress, ...)" ON)

  option(RUN_CMAKE_TEST "Run CMake test suite when built from sources" OFF)

  set(RUN_CMAKE_TEST_EXCLUDE "BootstrapTest" CACHE STRING "CMake test suite exclusion regex")

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
    if("${CMAKE_OSX_DEPLOYMENT_TARGET}" VERSION_LESS "10.10")
      message(FATAL_ERROR "Unsupported macOS deployment target: ${CMAKE_OSX_DEPLOYMENT_TARGET} is less than 10.10")
    else()
      set(binary_archive "macos10_10_binary")
    endif()
  endif()
  if(WIN32)
    set(binary_archive "win32_binary")
    if(CMAKE_SIZEOF_VOID_P EQUAL 8)
      if(${CMAKE_SYSTEM_PROCESSOR} STREQUAL "ARM64" OR "$ENV{SETUPTOOLS_EXT_SUFFIX}" MATCHES arm64)
        set(binary_archive "winarm64_binary")
      else()
        set(binary_archive "win64_binary")
      endif()
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

  # Add an external project step named `forceconfigure` to `project_name` ensuring
  # the project will always be reconfigured.
  #
  # Copied from ExternalProjectDependency.cmake (commontk/Artichoke@613e3739a)
  function(cpd_ExternalProject_AlwaysConfigure proj)
    _ep_get_step_stampfile(${proj} "configure" stampfile)
    ExternalProject_Add_Step(${proj} forceconfigure
      COMMAND ${CMAKE_COMMAND} -E remove ${stampfile}
      COMMENT "Forcing configure step for '${proj}'"
      DEPENDEES build
      ALWAYS 1
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

  set(ep_download_extract_timestamp_arg)
  if(CMAKE_VERSION VERSION_EQUAL "3.24" OR CMAKE_VERSION VERSION_GREATER "3.24")
    # See https://cmake.org/cmake/help/latest/policy/CMP0135.html
    set(ep_download_extract_timestamp_arg DOWNLOAD_EXTRACT_TIMESTAMP 1)
  endif()

  #
  # CMakeProject_SOURCE_DIR: Always expect the sources (needed for `sdist`)
  #
  if(NOT DEFINED CMakeProject_SOURCE_DIR)
    set(CMakeProject_SOURCE_DIR "${CMAKE_SOURCE_DIR}/CMake-src")

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
      ${ep_download_extract_timestamp_arg}
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

      # glibc check
      if(UNIX AND NOT APPLE)
        # as of CMake 3.23.0, the minimum supported version of libuv is 1.28.0.
        # this implies that the minimum supported glibc version is 2.12
        # https://github.com/libuv/libuv/blob/v1.x/SUPPORTED_PLATFORMS.md
        include(CheckSymbolExists)
        check_symbol_exists(__GLIBC__ "stdlib.h" HAS_GLIBC_MAJOR)
        check_symbol_exists(__GLIBC_MINOR__ "stdlib.h" HAS_GLIBC_MINOR)
        if(HAS_GLIBC_MAJOR AND HAS_GLIBC_MINOR AND (CMAKE_CXX_COMPILER_ID STREQUAL "GNU"))
          execute_process(COMMAND echo __GLIBC__ COMMAND "${CMAKE_CXX_COMPILER}" -E -P -imacros stdlib.h - OUTPUT_VARIABLE GLIBC_MAJOR_)
          string(STRIP "${GLIBC_MAJOR_}" GLIBC_MAJOR)
          execute_process(COMMAND echo __GLIBC_MINOR__ COMMAND "${CMAKE_CXX_COMPILER}" -E -P -imacros stdlib.h - OUTPUT_VARIABLE GLIBC_MINOR_)
          string(STRIP "${GLIBC_MINOR_}" GLIBC_MINOR)
          if("${GLIBC_MAJOR}.${GLIBC_MINOR}" VERSION_LESS "2.12")
            message(FATAL_ERROR "GLIBC ${GLIBC_MAJOR}.${GLIBC_MINOR} not supported")
          endif()
        endif()
      endif()

      # cmake cache arguments
      set(_cmake_cache_args)
      if(DEFINED CMAKE_BUILD_TYPE)
        list(APPEND _cmake_cache_args
          -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
          )
      endif()
      if(DEFINED CMAKE_TOOLCHAIN_FILE)
        list(APPEND _cmake_cache_args
          -DCMAKE_TOOLCHAIN_FILE:STRING=${CMAKE_TOOLCHAIN_FILE}
          )
      endif()
      foreach(var_name IN ITEMS
        CMAKE_BUILD_PARALLEL_LEVEL
        CMAKE_JOB_POOLS
        CMAKE_JOB_POOL_COMPILE
        CMAKE_JOB_POOL_LINK
        )
        if(DEFINED ${var_name})
          list(APPEND _cmake_cache_args
            -D${var_name}:STRING=${${var_name}}
            )
          message(STATUS "SuperBuild -   CMakeProject-build - ${var_name}: ${${var_name}}")
        endif()
      endforeach()

      if(DEFINED OPENSSL_ROOT_DIR)
        list(APPEND _cmake_cache_args
          -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT_DIR}
          )
        message(STATUS "SuperBuild -   CMakeProject-build - OPENSSL_ROOT_DIR: ${OPENSSL_ROOT_DIR}")
      endif()

      if(DEFINED CMAKE_CXX_STANDARD)
        list(APPEND _cmake_cache_args
          -DCMAKE_CXX_STANDARD:STRING=${CMAKE_CXX_STANDARD}
          )
        message(STATUS "SuperBuild -   CMakeProject-build - CMAKE_CXX_STANDARD: ${CMAKE_CXX_STANDARD}")
      endif()

      set(_cmake_args )
      if(UNIX AND (NOT APPLE AND NOT CMAKE_SYSTEM_NAME STREQUAL "FreeBSD"))
        # Since CMAKE_C_FLAGS and CMAKE_EXE_LINKER_FLAGS arguments contain spaces, we generate an initial
        # cache file.
        file(WRITE "${CMAKE_BINARY_DIR}/initial-cache.txt"
"set(CMAKE_C_FLAGS \"-D_POSIX_C_SOURCE=199506L -D_POSIX_SOURCE=1 -D_SVID_SOURCE=1 -D_BSD_SOURCE=1\" CACHE STRING \"Initial cache\" FORCE)
set(CMAKE_EXE_LINKER_FLAGS \"-lstdc++ -lgcc -lrt\" CACHE STRING \"Initial cache\" FORCE)
")
        set(_cmake_args
          CMAKE_ARGS -C "${CMAKE_BINARY_DIR}/initial-cache.txt"
          )
      endif()

      # cmake
      set(CMakeProject_BINARY_DIR ${CMAKE_BINARY_DIR}/CMakeProject-build)

      ExternalProject_add(CMakeProject-build
        SOURCE_DIR ${CMakeProject_SOURCE_DIR}
        BINARY_DIR ${CMakeProject_BINARY_DIR}
        DOWNLOAD_COMMAND ""
        UPDATE_COMMAND ""
        BUILD_ALWAYS 1
        ${_cmake_args}
        CMAKE_CACHE_ARGS
          -DBUILD_CursesDialog:BOOL=OFF
          -DCMAKE_USE_OPENSSL:BOOL=ON
          -DBUILD_TESTING:BOOL=ON
          -DCMake_INSTALL_DEPENDENCIES:BOOL=ON
          -DCMAKE_INSTALL_MESSAGE:STRING=NEVER
          ${_cmake_cache_args}
        USES_TERMINAL_CONFIGURE 1
        USES_TERMINAL_BUILD 1
        ${ep_log_configure_build_args}
        INSTALL_COMMAND ""
        DEPENDS
          CMakeProject-src-download
        )

        set(CMAKEPROJECT_BUILD_LAST_STEP "build")

        find_program(STRIP_EXECUTABLE strip)
        if(STRIP_EXECUTABLE)

          set(cmake_executable "${CMakeProject_BINARY_DIR}/bin/cmake")
          set(cpack_executable "${CMakeProject_BINARY_DIR}/bin/cpack")
          set(ctest_executable "${CMakeProject_BINARY_DIR}/bin/ctest")

          ExternalProject_Add_Step(CMakeProject-build strip_executables
            DEPENDEES ${CMAKEPROJECT_BUILD_LAST_STEP}
            COMMENT "Stripping CMake executables"
            COMMAND ${STRIP_EXECUTABLE} ${cmake_executable}
            COMMAND ${STRIP_EXECUTABLE} ${cpack_executable}
            COMMAND ${STRIP_EXECUTABLE} ${ctest_executable}
            USES_TERMINAL 1
            )
          set(CMAKEPROJECT_BUILD_LAST_STEP "strip_executables")
        endif()

        if(RUN_CMAKE_TEST)
          include(ProcessorCount)
          ProcessorCount(NB_CPU)
          if(NB_CPU EQUAL 0)
            set(NB_CPU 2)
          endif()
          ExternalProject_Add_Step(CMakeProject-build run_cmake_test_suite
            DEPENDEES ${CMAKEPROJECT_BUILD_LAST_STEP}
            COMMENT "Running CMake test suite, exclusion list: '${RUN_CMAKE_TEST_EXCLUDE}'"
            COMMAND ./bin/ctest --force-new-ctest-process --stop-on-failure --output-on-failure -j${NB_CPU} -E ${RUN_CMAKE_TEST_EXCLUDE}
            WORKING_DIRECTORY ${CMakeProject_BINARY_DIR}
            USES_TERMINAL 1
            )
          set(CMAKEPROJECT_BUILD_LAST_STEP "run_cmake_test_suite")
        endif()
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
      ${ep_download_extract_timestamp_arg}
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
    USES_TERMINAL_BUILD 1
    INSTALL_COMMAND ""
    DEPENDS
      ${${PROJECT_NAME}_DEPENDS}
    )
  message(STATUS "SuperBuild -   ${PROJECT_NAME}")

  cpd_ExternalProject_AlwaysConfigure(${PROJECT_NAME})

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

    if(APPLE)
      set(distribution_root "${CMakeProject_BINARY_DISTRIBUTION_DIR}/CMake.app/Contents")
    else()
      set(distribution_root "${CMakeProject_BINARY_DISTRIBUTION_DIR}")
    endif()

    # Install all files from binary distribution
    file(GLOB_RECURSE binary_distribution_files
      LIST_DIRECTORIES FALSE
      ${distribution_root}/*
      )
    foreach(file IN LISTS binary_distribution_files)
      # Skip symlinks like "CMake.app/Contents/Frameworks/QtWidgets.framework/Versions/Current"
      if(IS_SYMLINK ${file})
        continue()
      endif()

      # skip some mac app bundle files
      set(find_index -1)
      foreach(name IN ITEMS CodeResources Info.plist Frameworks _CodeSignature MacOS PlugIns Resources doc/cmake/html man)
        string(FIND "${file}" "${distribution_root}/${name}" find_index)
        if("${find_index}" EQUAL 0)
          break()
        endif()
      endforeach()
      if("${find_index}" EQUAL 0)
        continue()
      endif()

      get_filename_component(directory ${file} DIRECTORY)
      file(RELATIVE_PATH relative_directory ${distribution_root} ${directory})
      set(type FILES)
      if(relative_directory STREQUAL "bin")
        set(type PROGRAMS)
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
