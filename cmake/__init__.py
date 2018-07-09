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
    from skbuild.constants import CMAKE_INSTALL_DIR as SKBUILD_CMAKE_INSTALL_DIR
    _cmake_data = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', SKBUILD_CMAKE_INSTALL_DIR, 'cmake/data'))
    if os.path.exists(_cmake_data):
        CMAKE_DATA = _cmake_data

if platform.system().lower() == "darwin":
    CMAKE_DATA = os.path.join(CMAKE_DATA, 'CMake.app', 'Contents')

CMAKE_BIN_DIR = os.path.join(CMAKE_DATA, 'bin')
CMAKE_DOC_DIR = os.path.join(CMAKE_DATA, 'doc')
CMAKE_SHARE_DIR = os.path.join(CMAKE_DATA, 'share')


def _program(name, args):
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name)] + args)


def cmake():
    raise SystemExit(_program('cmake', sys.argv[1:]))


def cpack():
    raise SystemExit(_program('cpack', sys.argv[1:]))


def ctest():
    raise SystemExit(_program('ctest', sys.argv[1:]))
