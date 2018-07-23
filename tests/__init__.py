
import os
import sys

from contextlib import contextmanager


@contextmanager
def push_argv(argv):
    old_argv = sys.argv
    sys.argv = argv
    yield
    sys.argv = old_argv


def build_from_source():
    """Return True if CMake was built from source."""
    src_marker = os.path.join(os.path.dirname(__file__), "../src/CMakeLists.txt")
    return os.path.exists(src_marker)
