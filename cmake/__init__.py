import os
import platform
import subprocess
import sys

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

CMAKE_DATA = os.path.join(os.path.dirname(__file__), 'data')

# Support running tests from the source tree
if not os.path.exists(CMAKE_DATA):
    _cmake_data = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../_skbuild/cmake-install/cmake/data'))
    if os.path.exists(_cmake_data):
        CMAKE_DATA = _cmake_data

if platform.system().lower() == "darwin":
    CMAKE_DATA = os.path.join(CMAKE_DATA, 'CMake.app', 'Contents')

CMAKE_BIN_DIR = os.path.join(CMAKE_DATA, 'bin')
CMAKE_DOC_DIR = os.path.join(CMAKE_DATA, 'doc')
CMAKE_SHARE_DIR = os.path.join(CMAKE_DATA, 'share')


def _program(name, args):
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name)] + args)


def cmake(args):
    raise _program('cmake', args)


def cpack(args=None):
    raise _program('cpack', args)


def ctest(args=None):
    raise _program('ctest', args)


def _entrypoint_cmake():
    raise SystemExit(cmake(sys.argv[1:]))


def _entrypoint_cpack():
    raise SystemExit(cpack(sys.argv[1:]))


def _entrypoint_ctest():
    raise SystemExit(ctest(sys.argv[1:]))
