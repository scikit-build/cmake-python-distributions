import os

from scikit_build_core import build as _orig

if hasattr(_orig, "prepare_metadata_for_build_editable"):
    prepare_metadata_for_build_editable = _orig.prepare_metadata_for_build_editable
if hasattr(_orig, "prepare_metadata_for_build_wheel"):
    prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_editable = _orig.build_editable
build_wheel = _orig.build_wheel
build_sdist = _orig.build_sdist
get_requires_for_build_editable = _orig.get_requires_for_build_editable
get_requires_for_build_sdist = _orig.get_requires_for_build_sdist


def strtobool(value: str) -> bool:
    """
    Converts a environment variable string into a boolean value.
    """
    if not value:
        return False
    value = value.lower()
    if value.isdigit():
        return bool(int(value))
    return value not in {"n", "no", "off", "false", "f"}


def get_requires_for_build_wheel(config_settings=None):
    packages_orig = _orig.get_requires_for_build_wheel(config_settings)
    allow_cmake = strtobool(os.environ.get("CMAKE_PYTHON_DIST_ALLOW_CMAKE_DEP", ""))
    allow_ninja = any(
        strtobool(os.environ.get(var, ""))
        for var in ("CMAKE_PYTHON_DIST_FORCE_NINJA_DEP", "CMAKE_PYTHON_DIST_ALLOW_NINJA_DEP")
    )
    packages = []
    for package in packages_orig:
        package_name = package.lower().split(">")[0].strip()
        if package_name == "cmake" and not allow_cmake:
            msg = f"CMake PyPI distibution requires {package} to be available on the build system"
            raise ValueError(msg)
        if package_name == "ninja" and not allow_ninja:
            continue
        packages.append(package)
    return packages
