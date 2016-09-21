import os
import subprocess
import sys

CMAKE_BIN_DIR = os.path.join(os.path.dirname(__file__), 'data', 'bin')
CMAKE_DOC_DIR = os.path.join(os.path.dirname(__file__), 'data', 'doc')
CMAKE_SHARE_DIR = os.path.join(os.path.dirname(__file__), 'data', 'share')


def _program(name, args):
    return subprocess.call([os.path.join(CMAKE_BIN_DIR, name)] + args)


def cmake():
    raise SystemExit(_program('cmake', sys.argv[1:]))


def cpack():
    raise SystemExit(_program('cpack', sys.argv[1:]))


def ctest():
    raise SystemExit(_program('ctest', sys.argv[1:]))
