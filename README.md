# CMake Python Distributions

[![Build status](https://ci.appveyor.com/api/projects/status/439ila0jk7v6uqrr/branch/master?svg=true)](https://ci.appveyor.com/project/scikit-build/cmake-python-distributions-f3rbb/branch/master)
[![CircleCI](https://circleci.com/gh/scikit-build/cmake-python-distributions.svg?style=svg)](https://circleci.com/gh/scikit-build/cmake-python-distributions)
[![Build Status](https://travis-ci.org/scikit-build/cmake-python-distributions.svg?branch=master)](https://travis-ci.org/scikit-build/cmake-python-distributions)

This project provides a `setup.py` script that build CMake Python wheel. 

[CMake](http://www.cmake.org) is used to control the software compilation
process using simple platform and compiler independent configuration files, 
and generate native makefiles and workspaces that can be used in the
compiler environment of your choice.

The suite of CMake tools were created by Kitware in response to the need
for a powerful, cross-platform build environment for open-source projects
such as ITK and VTK.

## Building the CMake Python wheel module

Building the wheel requires:
* Git
* C++ Compiler
* Python
* [CMake](https://cmake.org)

Build the CMake Python wheel with the following command:

```
mkvirtualenv build-cmake
pip install -r requirements-dev.txt
python setup.py bdist_wheel
```

## Miscellaneous

This project is maintained by Jean-Christophe Fillion-Robin from Kitware Inc.

It is covered by the Apache License, Version 2.0:

http://www.apache.org/licenses/LICENSE-2.0

CMake is distributed under the OSI-approved BSD 3-clause License.

For more information about CMake, visit http://cmake.org
