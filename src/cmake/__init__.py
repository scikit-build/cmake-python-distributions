# -*- coding: utf-8 -*-
import os
import subprocess
import sys

from ._version import version as __version__

__all__ = ["__version__", "CMAKE_DATA", "CMAKE_BIN_DIR", "CMAKE_DOC_DIR", "CMAKE_SHARE_DIR", "cmake", "cpack", "ctest"]


def __dir__():
    return __all__


CMAKE_DATA = os.path.join(os.path.dirname(__file__), 'data')


# Support running tests from the source tree
if not os.path.exists(CMAKE_DATA):
    from skbuild.constants import CMAKE_INSTALL_DIR as SKBUILD_CMAKE_INSTALL_DIR
    from skbuild.constants import set_skbuild_plat_name

    if sys.platform.startswith("darwin"):
        # Since building the project specifying --plat-name or CMAKE_OSX_* variables
        # leads to different SKBUILD_DIR, the code below attempt to guess the most
        # likely plat-name.
        _skbuild_dirs = os.listdir(os.path.join(os.path.dirname(__file__), '..', '..', '_skbuild'))
        if _skbuild_dirs:
            _likely_plat_name = '-'.join(_skbuild_dirs[0].split('-')[:3])
            set_skbuild_plat_name(_likely_plat_name)

    _cmake_data = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', SKBUILD_CMAKE_INSTALL_DIR(), 'src/cmake/data'))
    if os.path.exists(_cmake_data):
        CMAKE_DATA = _cmake_data

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
