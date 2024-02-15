# -*- coding: utf-8 -*-
import os
import subprocess
import sys

from ._version import version as __version__

__all__ = ["__version__", "CMAKE_DATA", "CMAKE_BIN_DIR", "CMAKE_DOC_DIR", "CMAKE_SHARE_DIR", "cmake", "cpack", "ctest"]


def __dir__():
    return __all__


CMAKE_DATA = os.path.join(os.path.dirname(__file__), 'data')


assert os.path.exists(CMAKE_DATA)

CMAKE_BIN_DIR = os.path.join(CMAKE_DATA, 'bin')
CMAKE_DOC_DIR = os.path.join(CMAKE_DATA, 'doc')
CMAKE_SHARE_DIR = os.path.join(CMAKE_DATA, 'share')


def _program(name, args):
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name)] + args, close_fds=False)


def cmake():
    raise SystemExit(_program('cmake', sys.argv[1:]))


def cpack():
    raise SystemExit(_program('cpack', sys.argv[1:]))


def ctest():
    raise SystemExit(_program('ctest', sys.argv[1:]))
