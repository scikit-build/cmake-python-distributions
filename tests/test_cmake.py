# -*- coding: utf-8 -*-
import textwrap

import pytest

import cmake

from . import push_argv


def _run(program, args):
    func = getattr(cmake, program)
    args = ["%s.py" % program] + args
    with push_argv(args), pytest.raises(SystemExit) as excinfo:
        func()
    assert excinfo.value.code == 0


def test_cmake_module():
    _run("cmake", ["--version"])
    _run("cpack", ["--version"])
    _run("ctest", ["--version"])


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
