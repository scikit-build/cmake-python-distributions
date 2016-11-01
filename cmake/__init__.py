import os
import platform
import subprocess
import sys

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions

CMAKE_DATA = os.path.join(os.path.dirname(__file__), 'data')

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
