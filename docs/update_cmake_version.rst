====================
Update CMake version
====================

A developer should use the following steps to update the version ``X.Y.Z``
of CMake associated with the current CMake python distributions.

Available CMake archives can be found at https://cmake.org/files.


1. Install `requests` and `beautifulsoup4`::

    $ pip install requests beautifulsoup4

2. Execute `scripts/update_cmake_version.py` command line tool with the desired
   ``X.Y.Z`` CMake version available for download. For example::

    $ python scripts/update_cmake_version.py 3.7.1
    Collecting URLs and SHA256s from 'https://cmake.org/files/v3.7'
    Collecting URLs and SHA256s from 'https://cmake.org/files/v3.7' - done
    Updating 'CMakeUrls.cmake' with CMake version 3.7.1
    Updating 'CMakeUrls.cmake' with CMake version 3.7.1 - done
    Updating docs/index.rst
    Updating docs/index.rst - done
    Updating README.rst
    Updating README.rst - done
    Updating tests/test_wheel.py
    Updating tests/test_wheel.py - done

3. Create a topic named `update-to-cmake-X.Y.Z` and commit the changes

4. Create a `Pull Request`.

5. If all CI tests are passing, merge the topic and consider :doc:`making a new
   release </make_a_release>`.
