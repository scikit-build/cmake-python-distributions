==============================
Understanding the Build-system
==============================


The build system is described by the ``CMakeLists.txt`` and is composed of few projects each responsible
for a specific task. Once configured, the `Outer Project` is responsible for driving the overall build
composed of multiple project called `external project`. Here is the list of `external project`:

* ``CMakeProject-src-download``
* ``CMakeProject-binary-download``
* ``CMakeProject-build``
* ``CMakePythonDistributions``: This corresponds to the `Inner Project` represented below.

The flow chart represented below illustrates which external projects are included based on the configure
options and describes the role of each one:

.. mermaid::
    :align: center

    flowchart LR
        subgraph OP[Outer Project]
            style OP fill:#FFF0D7
            configure["CMakeLists.tct"]
            ask_download{"Download source?"}
            download_source["Download Source archive"]
            reuse_source_dir["Re-use source directory"]
            ask_build{"Build from Source?"}
            download_binaries["CMakeProject-binary-download"]
            build_cmake["CMakeProject-build"]
            strip_executables["Strip executables"]
            ask_inner_build{"Which files to install?"}
            install_pre_built["Install prebuilt binaries"]
            install_cmake_project["Install CMake project"]

            configure --> ask_download

            subgraph EP1[ExternalProject: CMakeProject-src-download]
                style EP1 fill:#E7CA92
                ask_download -->|yes| download_source
                ask_download -->|no| reuse_source_dir
            end

            download_source --> ask_build
            reuse_source_dir --> ask_build

            subgraph EP2[External Projects]
                style EP2 fill:#E7CA92
                ask_build -->|no| download_binaries
                ask_build -->|yes| build_cmake
                build_cmake --> strip_executables
            end

            download_binaries --> ask_inner_build
            strip_executables --> ask_inner_build

            subgraph IP[Inner Project: CMakePythonDistributions]
                style IP fill:#a1acc2
                ask_inner_build -->|no| install_pre_built
                ask_inner_build -->|yes| install_cmake_project
            end
        end


+----------------------------------------+--------------------------------------------------------------------------+
| **Node Title**                         | **Description**                                                          |
+========================================+==========================================================================+
| CMakeLists                             | CMake configuration file                                                 |
+----------------------------------------+--------------------------------------------------------------------------+
| Download source ?                      | If option ``CMakeProject_SOURCE_DIR`` is set, skip source download.      |
+----------------------------------------+--------------------------------------------------------------------------+
| Download Source archive                | External project downloading archives from https://cmake.org/files/.     |
+----------------------------------------+--------------------------------------------------------------------------+
| Re-use source directory                | Empty external project.                                                  |
+----------------------------------------+--------------------------------------------------------------------------+
| Build from Source ?                    | Answer based on option ``BUILD_CMAKE_FROM_SOURCE``                       |
+----------------------------------------+--------------------------------------------------------------------------+
| CMakeProject-binary-download           | External project downloading pre-built binary archives from              |
|                                        | https://cmake.org/files/.                                                |
+----------------------------------------+--------------------------------------------------------------------------+
| CMakeProject-build                     | External project building CMake from source.                             |
+----------------------------------------+--------------------------------------------------------------------------+
| Strip executables                      | If possible, reduce wheel size stripping cmake, cpack and ctest          |
|                                        | executables                                                              |
+----------------------------------------+--------------------------------------------------------------------------+
| Which files to install?                | Answer based on option ``BUILD_CMAKE_FROM_SOURCE``                       |
+----------------------------------------+--------------------------------------------------------------------------+
| Install prebuilt binaries              | Recursively glob all files and explicitly add install rules.             |
+----------------------------------------+--------------------------------------------------------------------------+
| Install CMake project                  | Achieved by including ``${CMakeProject_BINARY_DIR}/cmake_install.cmake`` |
+----------------------------------------+--------------------------------------------------------------------------+
