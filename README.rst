==========================
CMake Python Distributions
==========================

`CMake <http://www.cmake.org>`_ is used to control the software compilation
process using simple platform and compiler independent configuration files,
and generate native makefiles and workspaces that can be used in the
compiler environment of your choice.

The suite of CMake tools were created by Kitware in response to the need
for a powerful, cross-platform build environment for open-source projects
such as ITK and VTK.

The CMake python wheels provide `CMake 3.22.1 <https://cmake.org/cmake/help/v3.22/index.html>`_.

Latest Release
--------------

.. table::

  +----------------------------------------------------------------------+---------------------------------------------------------------------------+
  | Versions                                                             | Downloads                                                                 |
  +======================================================================+===========================================================================+
  | .. image:: https://img.shields.io/pypi/v/cmake.svg                   | .. image:: https://img.shields.io/badge/downloads-3997k%20total-green.svg |
  |     :target: https://pypi.python.org/pypi/cmake                      |     :target: https://pypi.python.org/pypi/cmake                           |
  +----------------------------------------------------------------------+---------------------------------------------------------------------------+

Build Status
------------

.. table::

  +---------------+--------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+
  |               | GitHub Actions (Windows, macOS, Linux)                                                                       | Travis CI (alternative archs)                                                               |
  +===============+==============================================================================================================+=============================================================================================+
  | PyPI          | .. image:: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml/badge.svg  | .. image:: https://travis-ci.com/scikit-build/cmake-python-distributions.svg?branch=master  |
  |               |     :target: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml          |     :target: https://travis-ci.com/github/scikit-build/cmake-python-distributions           |
  +---------------+--------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+

Platforms
---------

The following platforms are supported with binary wheels:

.. table::

  +---------------+--------------------------+
  | OS            | Arch                     |
  +===============+==========================+
  | Windows       | | 64-bit                 |
  |               | | 32-bit                 |
  +---------------+--------------------------+
  | Linux Intel   | | manylinux1+ 64-bit     |
  |               | | musllinux 64-bit       |
  |               | | manylinux1+ 32-bit     |
  |               | | musllinux 32-bit       |
  +---------------+--------------------------+
  | Linux ARM     | | manylinux2014+ AArch64 |
  |               | | musllinux AArch64      |
  +---------------+--------------------------+
  | Linux PowerPC | | manylinux2014+ ppc64le |
  |               | | musllinux ppc64le      |
  +---------------+--------------------------+
  | Linux IBM Z   | | manylinux2014+ s390x   |
  |               | | musllinux s390x        |
  +---------------+--------------------------+
  | macOS 10.10+  | Intel                    |
  +---------------+--------------------------+
  | macOS 11+     | Apple Silicon            |
  +---------------+--------------------------+

Maintainers
-----------

* `How to update CMake version? <http://cmake-python-distributions.readthedocs.io/en/latest/update_cmake_version.html>`_

* `How to make a release? <http://cmake-python-distributions.readthedocs.io/en/latest/make_a_release.html>`_

Miscellaneous
-------------

* Documentation: http://cmake-python-distributions.readthedocs.io/en/latest/
* Source code: https://github.com/scikit-build/cmake-python-distributions
* Mailing list: https://groups.google.com/forum/#!forum/scikit-build

License
-------

This project is maintained by Jean-Christophe Fillion-Robin from Kitware Inc.
It is covered by the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

CMake is distributed under the OSI-approved BSD 3-clause License.
For more information about CMake, visit http://cmake.org
