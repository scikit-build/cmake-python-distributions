
import os
import sys

from contextlib import contextmanager
from skbuild.constants import CMAKE_BUILD_DIR


@contextmanager
def push_argv(argv):
    old_argv = sys.argv
    sys.argv = argv
    yield
    sys.argv = old_argv


def build_from_source():
    """Return True if CMake was built from source."""
    marker = os.path.join(os.path.dirname(__file__), "..", CMAKE_BUILD_DIR, "CMakeProject-build")
    return os.path.exists(marker)
