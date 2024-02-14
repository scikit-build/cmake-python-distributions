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

.. blockdiag::
    :align: center
    :desctable:

    blockdiag {
        orientation = portrait
        node_width = 200;
        node_height = 60;


        group{
            label = "Outer Project";
            color = "#FFF0D7";

            // properties
            configure [shape = beginpoint, label = "CMakeLists", description="CMake configuration file"];
            ask_download [label ="Download source ?", shape = diamond, description = "If option ``CMakeProject_SOURCE_DIR`` is set, skip source download."];
            download_source [label ="Download Source archive", description = "External project downloading archives from https://cmake.org/files/."]
            reuse_source_dir [label ="Re-use source directory", description = "Empty external project."]

            // connections
            configure ->ask_download

            group{
                label = "ExternalProject: CMakeProject-src-download";
                color = "#E7CA92";
                ask_download ->  download_source [label = "yes"];
                ask_download -> reuse_source_dir  [label = "no"];
            }
            download_source -> ask_build
            reuse_source_dir -> ask_build

            // properties
            ask_build [label = "Build from Source ?", shape = diamond, description = "Answer based on option ``BUILD_CMAKE_FROM_SOURCE``"];
            download_binaries[label = "CMakeProject-binary-download", description = "External project downloading pre-built binary archives from https://cmake.org/files/."]
            build_cmake[label = "CMakeProject-build", description = "External project building CMake from source."]
            strip_executables[label = "Strip executables", description = "If possible, reduce wheel size stripping cmake, cpack and ctest executables"]

            // connections
            group{
                label = "External Projects";
                color = "#E7CA92";
                ask_build -> download_binaries [label = "no"];
                ask_build -> build_cmake [label = "yes"];
                build_cmake -> strip_executables
            }
            download_binaries -> ask_inner_build
            strip_executables -> ask_inner_build

            // properties
            ask_inner_build [label = "Which files to install?", shape = diamond, description = "Answer based on option ``BUILD_CMAKE_FROM_SOURCE``"];
            install_pre_built[label = "Install prebuilt binaries", description = "Recursively glob all files and explicitly add install rules."];
            install_cmake_project[label = "Install CMake project", description = "Achieved by including ``${CMakeProject_BINARY_DIR}/cmake_install.cmake``."];

            group{
                label = "Inner Project: CMakePythonDistributions";
                color = "#67789A";

                // connections
                ask_inner_build -> install_pre_built [label = "no"];
                ask_inner_build -> install_cmake_project [label = "yes"];
            }
        }
    }
