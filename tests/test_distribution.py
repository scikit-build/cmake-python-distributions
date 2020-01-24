
import os
import pytest
import textwrap

from path import Path

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dist'))


def _check_cmake_install(virtualenv, tmpdir):
    expected_version = "3.16.3"

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
    wheels = Path(DIST_DIR).files(match="*.whl")
    if not wheels:
        pytest.skip("no wheel available")
    assert len(wheels) == 1

    virtualenv.run("pip install %s" % wheels[0])

    _check_cmake_install(virtualenv, tmpdir)
