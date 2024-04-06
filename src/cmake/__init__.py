from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

if sys.version_info < (3, 8):
    from importlib_metadata import distribution
else:
    from importlib.metadata import distribution

from ._version import version as __version__

TYPE_CHECKING = False

if TYPE_CHECKING:
    from typing import Iterable, NoReturn


__all__ = ["__version__", "CMAKE_DATA", "CMAKE_BIN_DIR", "CMAKE_DOC_DIR", "CMAKE_SHARE_DIR", "cmake", "cpack", "ctest"]


def __dir__() -> list[str]:
    return __all__


cmake_executable_path = None
cmake_files = distribution("cmake").files
assert cmake_files is not None, "This is the cmake package so it must be installed and have files"
for script in cmake_files:
    if str(script).startswith("cmake/data/bin/cmake"):
        resolved_script = Path(script.locate()).resolve(strict=True)
        cmake_executable_path = resolved_script.parents[1]
        break
CMAKE_DATA = str(cmake_executable_path) if cmake_executable_path else None

assert CMAKE_DATA is not None
assert os.path.exists(CMAKE_DATA)

CMAKE_BIN_DIR = os.path.join(CMAKE_DATA, 'bin')
CMAKE_DOC_DIR = os.path.join(CMAKE_DATA, 'doc')
CMAKE_SHARE_DIR = os.path.join(CMAKE_DATA, 'share')


def _program(name: str, args: Iterable[str]) -> int:
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name), *args], close_fds=False)


def cmake() -> NoReturn:
    raise SystemExit(_program('cmake', sys.argv[1:]))


def cpack() -> NoReturn:
    raise SystemExit(_program('cpack', sys.argv[1:]))


def ctest() -> NoReturn:
    raise SystemExit(_program('ctest', sys.argv[1:]))
