===============================
Building the CMake Python wheel
===============================

Overview
--------

This project has been designed to work with `scikit-build <http://scikit-build.readthedocs.io/>`_.

It provides a `setup.py` and allows to create both source and binary distributions of
CMake.

This is done ensuring source files and build artifacts
are copied and/or generated in expected locations.


Prerequisites
-------------

In addition of ``Git``, ``Python`` and `CMake <https://cmake.org>`_, building
the wheel with ``BUILD_CMAKE_FROM_SOURCE`` set to ``ON`` also requires a
``C++ Compiler``.


Quick start
-----------

Build the CMake Python wheel with the following command::

    mkvirtualenv build-cmake
    pip install -r requirements-dev.txt
    python setup.py bdist_wheel


Source distribution (sdist)
---------------------------

CMake sources will always be downloaded in the ``<ROOT>/src``
directory.

This will ensure that the rules specified in ``<ROOT>/MANIFEST.in``
can successfully glob the source files.

The source distribution is generated using the following
command::

    python setup.py sdist


Binary distribution (build, bdist, bdist_wheel)
-----------------------------------------------

The project has two mode of operations:

#. build CMake from source  (``BUILD_CMAKE_FROM_SOURCE`` set to ``ON``)
#. download CMake binaries  (``BUILD_CMAKE_FROM_SOURCE`` set to ``OFF``)

The binary distribution is generated using the following
command::

    python setup.py bdist_wheel


Changing the default mode is achieved by explicitly passing the option
to CMake::

 python setup.py bdist_wheel -- -DBUILD_CMAKE_FROM_SOURCE:BOOL=ON


Default value for ``BUILD_CMAKE_FROM_SOURCE``
---------------------------------------------

Depending on the platform, option ``BUILD_CMAKE_FROM_SOURCE`` has
different default:

- Linux: ON
- MacOSX: OFF
- Windows: OFF

Controlling verbosity
---------------------

configure and build output
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the output associated to the configure and build steps of the
`CMakeProject-build` external project are logged into files. This can be
changed by setting the ``BUILD_VERBOSE`` option::

    python setup.py bdist_wheel -- -DBUILD_VERBOSE:BOOL=1

list of files copied into the distributions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, the complete list of files copied into the distributions are
reported. This can be changed passing the ``--hide-listing`` option::

    python setup.py --hide-listing sdist
    python setup.py --hide-listing bdist_wheel

Optimizations
-------------

On a given platform, when building different "flavor" of CMake python wheels (one
for each ``<python tag>-<abi>`` tag), the whole process can be made faster in two
ways.

Caching downloads
^^^^^^^^^^^^^^^^^

To avoid the re-download of CMake sources and/or binary packages, passing the
option ``-DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/path/to/cache``
enables successive build to re-use existing archives instead of re-downloading them.

Re-using build tree
^^^^^^^^^^^^^^^^^^^

And finally, on a given platform, to avoid rebuilding CMake, the idea is to
first create a standalone build of the CMake project and then building the
wheel using it.

Step 1: Standalone build::

    mkdir -p standalone-build && cd $_
    cmake -DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/path/to/cache -G Ninja ../

Step 2: Faster build reusing download and build directories::

    python setup.py bdist_wheel -- \
       -DCMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR:PATH=/path/to/cache \
       -DCMakeProject_BINARY_DIR:PATH=/path/to/standalone-build
