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

Classic procedure
-----------------

1. Execute the `scripts/update_cmake_version.py` command line tool with the
   desired ``X.Y.Z`` CMake version available for download (the script carries
   inline dependency metadata, so ``uv run`` handles the ``requests``
   dependency). For example::

    $ uv run scripts/update_cmake_version.py 4.4.0
    Collecting URLs and SHA256s from 'https://api.github.com/repos/Kitware/CMake/releases/tags/v4.4.0'
    [...]

   It updates ``CMakeUrls.cmake``, ``pyproject.toml``, ``README.rst``,
   ``tests/test_cmake.py``, and the version references in ``docs/``, then
   prints the commands for the next step.

2. Run the printed commands to create a topic named `update-to-cmake-X.Y.Z`,
   commit the changes, and create a `Pull Request`.

3. If all CI tests are passing, merge the topic and consider :doc:`making a new
   release </make_a_release>`.
