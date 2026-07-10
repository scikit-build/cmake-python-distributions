=====
Usage
=====

After :doc:`installing </installation>` the package, the executables ``cmake``,
``cpack``, ``ctest``, and ``ccmake`` will be available in the ``PATH`` and can
be used to configure and build any project. ``ccmake`` (the curses-based
interactive interface) is not included on Windows.

You can also run ``python -m cmake ...`` to invoke ``cmake`` explicitly through
a specific Python installation.

The ``cmake`` module exposes the location of the bundled installation as
``cmake.CMAKE_DATA``, ``cmake.CMAKE_BIN_DIR``, ``cmake.CMAKE_DOC_DIR``, and
``cmake.CMAKE_SHARE_DIR``, along with ``cmake.__version__``.
