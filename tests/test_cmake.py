import os
import subprocess
import sys
import sysconfig
import textwrap

import pytest

if sys.version_info < (3, 8):
    from importlib_metadata import distribution
else:
    from importlib.metadata import distribution

import cmake

from . import push_argv

all_tools = pytest.mark.parametrize("tool", ["cmake", "cpack", "ctest"])


def _run(program, args):
    func = getattr(cmake, program)
    args = [f"{program}.py", *args]
    with push_argv(args), pytest.raises(SystemExit) as excinfo:
        func()
    assert excinfo.value.code == 0


@all_tools
def test_cmake_module(tool):
    _run(tool, ["--version"])


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

    _run("cmake", [f"-DTMP_DIR:PATH={tmpdir}", "-P", str(test_script)])


def _get_scripts():
    dist = distribution("cmake")
    scripts_paths = [os.path.abspath(sysconfig.get_path("scripts", scheme)) for scheme in sysconfig.get_scheme_names()]
    scripts = []
    for file in dist.files:
        if os.path.abspath(str(file.locate().parent)) in scripts_paths:
            scripts.append(file.locate().resolve(strict=True))
    return scripts


@all_tools
def test_cmake_script(tool):
    expected_version = "3.30.0"
    scripts = [script for script in _get_scripts() if script.stem == tool]
    assert len(scripts) == 1
    output = subprocess.check_output([str(scripts[0]), "--version"]).decode("ascii")
    assert output.splitlines()[0] == f"{tool} version {expected_version}"


def test_cmake_main():
    expected_version = "3.30.0"
    output = subprocess.run([sys.executable, "-m", "cmake", "--version"], text=True, capture_output=True, check=False).stdout
    assert output.splitlines()[0] == f"cmake version {expected_version}"
