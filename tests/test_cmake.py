
import pytest

import cmake

from . import push_argv


def test_cmake_module():
    with push_argv(["cmake.py", "--version"]), pytest.raises(SystemExit):
        cmake.cmake()

    with push_argv(["cpack.py", "--version"]), pytest.raises(SystemExit):
        cmake.cpack()

    with push_argv(["ctest.py", "--version"]), pytest.raises(SystemExit):
        cmake.ctest()
