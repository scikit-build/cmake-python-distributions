
import os
import pytest
import textwrap

from packaging.version import parse as parse_version
from packaging.version import Version
from path import Path

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dist'))


def _check_cmake_install(virtualenv, tmpdir):
    expected_version = "3.12.0"
    # Expected output for CMake < 2.8.0 (see https://github.com/Kitware/CMake/commit/98c51ff)
    if parse_version(expected_version) < Version("2.8.0"):
        expected_version = "%s.%s-patch %s" % tuple(expected_version.split("."))

    for executable_name in ["cmake", "cpack", "ctest"]:
        output = virtualenv.run(
            "%s --version" % executable_name, capture=True).splitlines()[0]
        assert output == "%s version %s" % (executable_name, expected_version)

    test_script = tmpdir.join("test_cmake.cmake")
    test_script.write(textwrap.dedent(r"""
        message("${CMAKE_COMMAND}")
        """))

    output = virtualenv.run("cmake -P %s" % str(test_script), capture=True)
    expected = os.path.realpath(virtualenv.virtualenv).replace(os.sep, "/")
    assert output[:len(expected)].lower() == expected.lower()


@pytest.mark.skipif(not Path(DIST_DIR).exists(), reason="dist directory does not exist")
def test_wheel(virtualenv, tmpdir):
    wheels = Path(DIST_DIR).files(pattern="*.whl")
    if not wheels:
        pytest.skip("no wheel available")
    assert len(wheels) == 1

    virtualenv.run("pip install %s" % wheels[0])

    _check_cmake_install(virtualenv, tmpdir)
