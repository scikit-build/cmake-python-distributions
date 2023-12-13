.. _updating_cmake_version:

==========================
Updating the CMake version
==========================

A developer should use the following steps to update the version ``X.Y.Z``
of CMake associated with the current CMake python distributions.

Available CMake archives can be found at https://cmake.org/files.

Nox procedure
-------------

If using nox, run::

    nox -s bump -- <version>


And follow the instructions it gives you. Leave off the version to bump to the latest version. Add `--commit` to run the commit procedure.

Classic procedure:
------------------

1. Install `requests`::

    $ pip install requests

2. Execute `scripts/update_cmake_version.py` command line tool with the desired
   ``X.Y.Z`` CMake version available for download. For example::

    $ release=3.28.0
    $ ./scripts/update_cmake_version.py $release
    Collecting URLs and SHA256s from 'https://api.github.com/repos/Kitware/CMake/releases/tags/v3.28.0'
    [...]
    Collecting URLs and SHA256s from 'https://api.github.com/repos/Kitware/CMake/releases/tags/v3.28.0' - done
    Updating 'CMakeUrls.cmake' with CMake version 3.28.0
    Updating 'CMakeUrls.cmake' with CMake version 3.28.0 - done
    Updating docs/index.rst
    Updating docs/index.rst - done
    Updating README.rst
    Updating README.rst - done
    Updating tests/test_cmake.py
    Updating tests/test_cmake.py - done

3. Create a topic named `update-to-cmake-X.Y.Z` and commit the changes.
   For example::

    release=3.28.0
    git switch -c update-to-cmake-$release
    git add -u CMakeUrls.cmake docs/index.rst README.rst tests/test_cmake.py docs/update_cmake_version.rst
    git commit -m "Update to CMake $release"

4. Push the topic and create a `Pull Request`.

5. If all CI tests are passing, merge the topic and consider :doc:`making a new
   release </make_a_release>`.
