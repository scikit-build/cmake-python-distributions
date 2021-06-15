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

The CMake python wheels provide `CMake 3.20.4 <https://cmake.org/cmake/help/v3.20/index.html>`_.

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

  +---------------+------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+
  |               | Linux                                                                                    | macOS                                                                                       | Windows                                                                                                   |
  +===============+==========================================================================================+=============================================================================================+===========================================================================================================+
  | PyPI          | .. image:: https://circleci.com/gh/scikit-build/cmake-python-distributions.svg?style=svg | .. image:: https://travis-ci.com/scikit-build/cmake-python-distributions.svg?branch=master  | .. image:: https://ci.appveyor.com/api/projects/status/439ila0jk7v6uqrr/branch/master?svg=true            |
  |               |     :target: https://circleci.com/gh/scikit-build/cmake-python-distributions             |     :target: https://travis-ci.com/github/scikit-build/cmake-python-distributions           |    :target: https://ci.appveyor.com/project/scikit-build/cmake-python-distributions-f3rbb/branch/master   |
  +---------------+------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------+

Platforms
---------

The following platforms are supported with binary wheels:

.. table::

  +--------------+------------------------+
  | OS           | Arch                   |
  +==============+========================+
  | Windows      | 64-bit                 |
  +--------------+------------------------+
  | Windows      | 32-bit                 |
  +--------------+------------------------+
  | Linux        | manylinux1+ 64-bit     |
  +--------------+------------------------+
  | Linux        | manylinux1+ 32-bit     |
  +--------------+------------------------+
  | Linux ARM    | manylinux2014+ AArch64 |
  +--------------+------------------------+
  | Linux        | manylinux2014+ ppc64le |
  +--------------+------------------------+
  | Linux        | manylinux2014+ s390x   |
  +--------------+------------------------+
  | macOS 10.10+ | Intel                  |
  +--------------+------------------------+
  | macOS 11+    | Apple Silicon          |
  +--------------+------------------------+

Until `PEP 656 <https://www.python.org/dev/peps/pep-0656/>`_ is implemented, we
cannot provide wheels for Alpine and other MUSL variants. If you need to use
Alpine, the requirements are ``g++ ninja cmake openssl-dev linux-headers``. If
those are installed, then `pip3 install cmake`` will work.

Maintainers
-----------

* `How to update CMake version ? <http://cmake-python-distributions.readthedocs.io/en/latest/update_cmake_version.html>`_

* `How to make a release ? <http://cmake-python-distributions.readthedocs.io/en/latest/make_a_release.html>`_

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
