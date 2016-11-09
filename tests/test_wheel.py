
import os
import textwrap

from path import Path

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../dist'))


def test_command_line(virtualenv, tmpdir):
    wheels = Path(DIST_DIR).files(pattern="*.whl")
    assert len(wheels) == 1

    virtualenv.install_package("coverage==4.2")
    virtualenv.run("pip install %s" % wheels[0])

    expected_version = "3.6.2"

    for executable_name in ["cmake", "cpack", "ctest"]:
        output = virtualenv.run(
            "%s --version" % executable_name, capture=True).splitlines()[0]
        assert output == "%s version %s" % (executable_name, expected_version)

    test_script = tmpdir.join("test_cmake.cmake")
    test_script.write(textwrap.dedent(r"""
    message("${CMAKE_COMMAND}")
    """))

    output = virtualenv.run("cmake -P %s" % str(test_script), capture=True)
    assert output.startswith(
        os.path.realpath(virtualenv.virtualenv).replace(os.sep, "/"))
