import os
import subprocess
import sys

if sys.version_info < (3, 8):
    from importlib_metadata import distribution
else:
    from importlib.metadata import distribution

from ._version import version as __version__

__all__ = ["__version__", "CMAKE_DATA", "CMAKE_BIN_DIR", "CMAKE_DOC_DIR", "CMAKE_SHARE_DIR", "cmake", "cpack", "ctest"]


def __dir__():
    return __all__


cmake_executable_path = None
for script in distribution("cmake").files:
    if str(script).startswith("cmake/data/bin/cmake"):
        resolved_script = script.locate().resolve(strict=True)
        cmake_executable_path = resolved_script.parents[1]
        break
CMAKE_DATA = str(cmake_executable_path) if cmake_executable_path else None

assert CMAKE_DATA is not None
assert os.path.exists(CMAKE_DATA)

CMAKE_BIN_DIR = os.path.join(CMAKE_DATA, 'bin')
CMAKE_DOC_DIR = os.path.join(CMAKE_DATA, 'doc')
CMAKE_SHARE_DIR = os.path.join(CMAKE_DATA, 'share')


def _program(name, args):
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name), *args], close_fds=False)


def cmake():
    raise SystemExit(_program('cmake', sys.argv[1:]))


def cpack():
    raise SystemExit(_program('cpack', sys.argv[1:]))


def ctest():
    raise SystemExit(_program('ctest', sys.argv[1:]))
