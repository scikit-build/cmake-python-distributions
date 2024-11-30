from __future__ import annotations

import os

from scikit_build_core import build as _orig

if hasattr(_orig, "prepare_metadata_for_build_editable"):
    prepare_metadata_for_build_editable = _orig.prepare_metadata_for_build_editable
if hasattr(_orig, "prepare_metadata_for_build_wheel"):
    prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_editable = _orig.build_editable
build_sdist = _orig.build_sdist
get_requires_for_build_editable = _orig.get_requires_for_build_editable
get_requires_for_build_sdist = _orig.get_requires_for_build_sdist


def _strtobool(value: str) -> bool:
    """
    Converts a environment variable string into a boolean value.
    """
    if not value:
        return False
    value = value.lower()
    if value.isdigit():
        return bool(int(value))
    return value not in {"n", "no", "off", "false", "f"}


def get_requires_for_build_wheel(
    config_settings: dict[str, str | list[str]] | None = None,
) -> list[str]:
    packages_orig = _orig.get_requires_for_build_wheel(config_settings)
    allow_cmake = _strtobool(os.environ.get("CMAKE_PYTHON_DIST_ALLOW_CMAKE_DEP", ""))
    allow_ninja = any(
        _strtobool(os.environ.get(var, ""))
        for var in ("CMAKE_PYTHON_DIST_FORCE_NINJA_DEP", "CMAKE_PYTHON_DIST_ALLOW_NINJA_DEP")
    )
    packages = []
    for package in packages_orig:
        package_name = package.lower().split(">")[0].strip()
        if package_name == "cmake" and not allow_cmake:
            continue
        if package_name == "ninja" and not allow_ninja:
            continue
        packages.append(package)
    return packages


def _bootstrap_build(temp_path: str, config_settings: dict[str, list[str] | str] | None = None) -> str:
    import hashlib
    import re
    import shutil
    import subprocess
    import tarfile
    import urllib.request
    from pathlib import Path

    env = os.environ.copy()
    temp_path_ = Path(temp_path)

    if "MAKE" not in env:
        make_path = None
        make_candidates = ("gmake", "make", "smake")
        for candidate in make_candidates:
            make_path = shutil.which(candidate)
            if make_path is not None:
                break
        if make_path is None:
            msg = f"Could not find a make program. Tried {make_candidates!r}"
            raise ValueError(msg)
        env["MAKE"] = make_path
    make_path = env["MAKE"]

    archive_path = temp_path_
    if config_settings:
        archive_path = Path(config_settings.get("cmake.define.CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR", archive_path))
        archive_path.mkdir(parents=True, exist_ok=True)

    cmake_urls = Path("CMakeUrls.cmake").read_text()
    source_url = re.findall(r'set\(unix_source_url\s+"(?P<data>.*)"\)$', cmake_urls, flags=re.MULTILINE)[0]
    source_sha256 = re.findall(r'set\(unix_source_sha256\s+"(?P<data>.*)"\)$', cmake_urls, flags=re.MULTILINE)[0]

    tarball_name = source_url.rsplit("/", maxsplit=1)[1]
    assert tarball_name.endswith(".tar.gz")
    source_tarball = archive_path / tarball_name
    if not source_tarball.exists():
        with urllib.request.urlopen(source_url) as response:
            source_tarball.write_bytes(response.read())

    sha256 = hashlib.sha256(source_tarball.read_bytes()).hexdigest()
    if source_sha256.lower() != sha256.lower():
        msg = f"Invalid sha256 for {source_url!r}. Expected {source_sha256!r}, got {sha256!r}"
        raise ValueError(msg)

    tar_filter_kwargs = {"filter": "tar"} if hasattr(tarfile, "tar_filter") else {}
    with tarfile.open(source_tarball) as tar:
        tar.extractall(path=temp_path_, **tar_filter_kwargs)

    parallel_str = env.get("CMAKE_BUILD_PARALLEL_LEVEL", "1")
    parallel = max(0, int(parallel_str) if parallel_str.isdigit() else 1) or os.cpu_count() or 1

    bootstrap_path = next(temp_path_.glob("cmake-*/bootstrap"))
    prefix_path = temp_path_ / "cmake-install"
    bootstrap_args = [f"--prefix={prefix_path}", "--no-qt-gui", "--no-debugger", "--parallel={parallel}", "--", "-DBUILD_TESTING=OFF", "-DBUILD_CursesDialog:BOOL=OFF"]
    previous_cwd = Path().absolute()
    os.chdir(bootstrap_path.parent)
    try:
        subprocess.run([bootstrap_path, *bootstrap_args], env=env, check=True)
        subprocess.run([make_path, "-j", f"{parallel}"], env=env, check=True)
        subprocess.run([make_path, "install"], env=env, check=True)
    finally:
        os.chdir(previous_cwd)

    return str(prefix_path / "bin" / "cmake")


def build_wheel(
    wheel_directory: str,
    config_settings: dict[str, list[str] | str] | None = None,
    metadata_directory: str | None = None,
) -> str:
    from scikit_build_core.errors import CMakeNotFoundError

    try:
        return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
    except CMakeNotFoundError:
        if os.name != "posix":
            raise
    # Let's try bootstrapping CMake
    import tempfile
    with tempfile.TemporaryDirectory() as temp_path:
        cmake_path = _bootstrap_build(temp_path, config_settings)
        assert cmake_path
        os.environ["CMAKE_EXECUTABLE"] = cmake_path
        return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)