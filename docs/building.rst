===============================
Building the CMake Python wheel
===============================

Overview
--------

This project is built with `scikit-build-core <https://scikit-build-core.readthedocs.io/>`_,
using a custom build backend (in ``_build_backend``) that removes the ``cmake``
and ``ninja`` build requirements and can bootstrap CMake if it is not already
available on the system.


Prerequisites
-------------

Building the wheel requires ``Git`` and ``Python``. Building with
``BUILD_CMAKE_FROM_SOURCE`` set to ``ON`` also requires a C++ compiler and a
make program. An existing `CMake <https://cmake.org>`_ installation is used if
found; otherwise one is bootstrapped automatically (built from source on POSIX
systems, or downloaded as a prebuilt binary on Windows).


Quick start
-----------

Build the CMake Python wheel with the following commands::

    python3 -m venv .venv
    source .venv/bin/activate
    pip install build
    python -m build --wheel

Or, using `uv <https://docs.astral.sh/uv/>`_::

    uv build --wheel

Note that wheels produced this way are only usable locally; the redistributable
wheels on PyPI are produced with `cibuildwheel <https://cibuildwheel.pypa.io>`_
(see ``.github/workflows/build.yml``).


Source distribution (sdist)
---------------------------

The source distribution contains this project's sources plus the CMake source
tarball listed in ``CMakeUrls.cmake``, bundled as
``archive-cache/cmake-<version>.tar.gz``. Building the sdist downloads that
tarball, so it needs network access; building a wheel from the sdist with
``BUILD_CMAKE_FROM_SOURCE=ON`` (the default on Linux) does not.

``BUILD_CMAKE_FROM_SOURCE=OFF`` (the default on macOS and Windows) still
downloads a prebuilt binary archive at wheel-build time.

The source distribution is generated using the following command::

    python -m build --sdist


Binary distribution (wheel)
---------------------------

The project has two modes of operation:

#. build CMake from source  (``BUILD_CMAKE_FROM_SOURCE`` set to ``ON``)
#. download CMake binaries  (``BUILD_CMAKE_FROM_SOURCE`` set to ``OFF``)

The binary distribution is generated using the following
command::

    python -m build --wheel


Changing the default mode is achieved by explicitly passing the option
to CMake::

    python -m build --wheel -Ccmake.define.BUILD_CMAKE_FROM_SOURCE=ON


Default value for ``BUILD_CMAKE_FROM_SOURCE``
---------------------------------------------

Depending on the platform, option ``BUILD_CMAKE_FROM_SOURCE`` has
a different default:

- Linux: ``ON``
- macOS: ``OFF``
- Windows: ``OFF``

Controlling verbosity
---------------------

By default, the output associated with the configure and build steps of the
``CMakeProject-build`` external project is displayed, along with download
progress. Setting ``BUILD_VERBOSE`` to ``OFF`` logs the configure and build
output to files instead::

   python -m build --wheel -Ccmake.define.BUILD_VERBOSE=OFF


Optimizations
-------------

On a given platform, when building different "flavors" of CMake python wheels
(one for each ``<python tag>-<abi>`` tag), the whole process can be made faster
in two ways.

Caching downloads
^^^^^^^^^^^^^^^^^

Archives are downloaded into ``archive-cache/`` in the source tree (gitignored)
and re-used by later builds when their hash matches. To use a different
location, pass
``-Ccmake.define.CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR=/path/to/cache``.

Re-using the build tree
^^^^^^^^^^^^^^^^^^^^^^^

And finally, on a given platform, to avoid rebuilding CMake, the idea is to
first create a standalone build of the CMake project and then build the
wheel using it.

Step 1: Standalone build::

    mkdir -p standalone-build && cd $_
    cmake -DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/path/to/cache -G Ninja ../

Step 2: Faster build reusing download and build directories::

    python -m build --wheel \
        -Ccmake.define.CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR=/path/to/cache \
        -Ccmake.define.CMakeProject_BINARY_DIR=/path/to/standalone-build
