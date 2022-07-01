from typing import NoReturn

__version__: tuple[int, int, int] | tuple[int, int, int, str, str]

CMAKE_DATA: str

CMAKE_BIN_DIR: str
CMAKE_DOC_DIR: str
CMAKE_SHARE_DIR: str

def _program(name: str, args: Iterator[str]) -> int: ...

def cmake() -> NoReturn: ...
def cpack() -> NoReturn: ...
def ctest() -> NoReturn: ...
