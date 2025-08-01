==========================
CMake Python Distributions
==========================

`CMake <https://cmake.org>`_ is used to control the software compilation
process using simple platform and compiler independent configuration files,
and generate native makefiles and workspaces that can be used in the
compiler environment of your choice.

The suite of CMake tools were created by Kitware in response to the need
for a powerful, cross-platform build environment for open-source projects
such as ITK and VTK.

The CMake python wheels provide `CMake 4.0.3 <https://cmake.org/cmake/help/v4.0/index.html>`_.

Latest Release
--------------

.. table::

  +----------------------------------------------------------------------+---------------------------------------------------------------------------+
  | Versions                                                             | Downloads                                                                 |
  +======================================================================+===========================================================================+
  | .. image:: https://img.shields.io/pypi/v/cmake.svg                   | .. image:: https://static.pepy.tech/badge/cmake                           |
  |     :target: https://pypi.python.org/pypi/cmake                      |     :target: https://pypi.python.org/pypi/cmake                           |
  |                                                                      | .. image:: https://img.shields.io/pypi/dm/cmake                           |
  |                                                                      |     :target: https://pypi.python.org/pypi/cmake                           |
  +----------------------------------------------------------------------+---------------------------------------------------------------------------+

Build Status
------------

.. table::

  +---------------+--------------------------------------------------------------------------------------------------------------+
  |               | GitHub Actions (Windows, macOS, Linux)                                                                       |
  +===============+==============================================================================================================+
  | PyPI          | .. image:: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml/badge.svg  |
  |               |     :target: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml          |
  +---------------+--------------------------------------------------------------------------------------------------------------+

Platforms
---------

The following platforms are supported with binary wheels:

.. table::

  +---------------+---------------------------+
  | OS            | Arch                      |
  +===============+===========================+
  | Windows       | | 64-bit                  |
  |               | | 32-bit                  |
  +---------------+---------------------------+
  | Linux Intel   | | manylinux2010+  x86_64  |
  |               | | musllinux_1_1+  x86_64  |
  |               | | manylinux2010+  i686    |
  |               | | musllinux_1_1+  i686    |
  +---------------+---------------------------+
  | Linux ARM     | | manylinux2014+  AArch64 |
  |               | | musllinux_1_1+  AArch64 |
  |               | | manylinux_2_31+ armv7l  |
  |               | | musllinux_1_2+  armv7l  |
  +---------------+---------------------------+
  | Linux PowerPC | | manylinux2014+  ppc64le |
  |               | | musllinux_1_1+  ppc64le |
  +---------------+---------------------------+
  | Linux IBM Z   | | manylinux2014+  s390x   |
  |               | | musllinux_1_1+  s390x   |
  +---------------+---------------------------+
  | Linux RISC-V  | | manylinux_2_39+ riscv64 |
  |               | | musllinux_1_2+  riscv64 |
  +---------------+---------------------------+
  | macOS 10.10+  | Intel                     |
  +---------------+---------------------------+
  | macOS 11+     | Apple Silicon             |
  +---------------+---------------------------+

The last version to provide ``manylinux1`` wheels was ``3.22.x``.
The last version to provide Python 2 to Python 3.6 support was ``3.28.x``.

Maintainers
-----------

* `How to update CMake version? <https://cmake-python-distributions.readthedocs.io/en/latest/update_cmake_version.html>`_

* `How to make a release? <https://cmake-python-distributions.readthedocs.io/en/latest/make_a_release.html>`_

Miscellaneous
-------------

* Documentation: https://cmake-python-distributions.readthedocs.io/en/latest/
* Source code: https://github.com/scikit-build/cmake-python-distributions
* Mailing list: https://groups.google.com/forum/#!forum/scikit-build

License
-------

This project is maintained by Jean-Christophe Fillion-Robin from Kitware Inc.
It is covered by the `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.

CMake is distributed under the OSI-approved BSD 3-clause License.
For more information about CMake, visit https://cmake.org
