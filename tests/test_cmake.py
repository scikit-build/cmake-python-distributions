
import textwrap
import platform
import pytest

import cmake

from packaging.version import parse as parse_version
from packaging.version import Version

from . import build_from_source, push_argv


def _run(program, args):
    func = getattr(cmake, program)
    args = ["%s.py" % program] + args
    with push_argv(args), pytest.raises(SystemExit) as excinfo:
        func()
    assert 0 == excinfo.value.code


def test_cmake_module():
    _run("cmake", ["--version"])
    _run("cpack", ["--version"])
    _run("ctest", ["--version"])


print(">>>>>>>>>>>>>>>>>>>> build_from_source [%s]" % build_from_source())
print(">>>>>>>>>>>>>>>>>>>> cmake_version [%s]" % cmake.__version__)
print(">>>>>>>>>>>>>>>>>>>> plat [%s]" % platform.system().lower())
print(">>>>>>>>>>>>>>>>>>>> version_cmp [%s]" % (parse_version(cmake.__version__) < Version("3.7.2")))


@pytest.mark.skipif(
    (not build_from_source()
     and platform.system().lower() == "darwin"
     and parse_version(cmake.__version__) < Version("3.7.2")),
    reason="SSL support is broken in macOS CMake binaries <= 3.7.1"
)
def test_cmake_https(tmpdir):
    test_script = tmpdir.join("cmake-test-https-download.cmake")
    test_script.write(textwrap.dedent(
        """
        file(
          DOWNLOAD
            https://github.com/scikit-build/cmake-python-distributions
            ${TMP_DIR}/page.html
          SHOW_PROGRESS
          STATUS status
          )
        list(GET status 0 error_code)
        list(GET status 1 error_msg)
        if(error_code)
            message(
                FATAL_ERROR "error: Failed to download ${url}: ${error_msg}")
        endif()
        """
    ))

    _run("cmake", ["-DTMP_DIR:PATH=%s" % str(tmpdir), "-P", str(test_script)])
