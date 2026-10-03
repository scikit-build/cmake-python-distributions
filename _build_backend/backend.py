from __future__ import annotations

import os
from pathlib import Path

from scikit_build_core import build as _orig

# Archives are downloaded here (gitignored). The sdist bundles the unix source
# tarball in this directory so a build from the sdist needs no network.
_ARCHIVE_DIR = Path("archive-cache")

if hasattr(_orig, "prepare_metadata_for_build_editable"):
    prepare_metadata_for_build_editable = _orig.prepare_metadata_for_build_editable
if hasattr(_orig, "prepare_metadata_for_build_wheel"):
    prepare_metadata_for_build_wheel = _orig.prepare_metadata_for_build_wheel
build_editable = _orig.build_editable
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


def _fetch_archive(kind: str, archive_dir: Path) -> Path:
    """
    Return the path to the ``kind`` archive listed in ``CMakeUrls.cmake``,
    downloading it into ``archive_dir`` if it is not already there. The SHA256
    is always verified.
    """
    import hashlib
    import re
    import urllib.request

    cmake_urls = Path("CMakeUrls.cmake").read_text()
    archive_url = re.findall(rf'set\({kind}_url\s+"(?P<data>.*)"\)$', cmake_urls, flags=re.MULTILINE)[0]
    archive_sha256 = re.findall(rf'set\({kind}_sha256\s+"(?P<data>.*)"\)$', cmake_urls, flags=re.MULTILINE)[0]

    archive_name = archive_url.rsplit("/", maxsplit=1)[1]
    archive_path = archive_dir / archive_name
    if not archive_path.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(archive_url) as response:
            archive_path.write_bytes(response.read())

    sha256 = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    if archive_sha256.lower() != sha256.lower():
        msg = f"Invalid sha256 for {archive_url!r}. Expected {archive_sha256!r}, got {sha256!r}"
        raise ValueError(msg)

    return archive_path


def build_sdist(
    sdist_directory: str,
    config_settings: dict[str, list[str] | str] | None = None,
) -> str:
    archive_path = _fetch_archive("unix_source", _ARCHIVE_DIR)

    settings: dict[str, list[str] | str] = dict(config_settings or {})
    include = settings.get("sdist.include", [])
    if isinstance(include, str):
        include = include.split(";")
    settings["sdist.include"] = [*include, archive_path.as_posix()]
    return _orig.build_sdist(sdist_directory, settings)


def _bootstrap_build(temp_path: str, config_settings: dict[str, list[str] | str] | None = None) -> str:
    import platform
    import shutil
    import subprocess
    import tarfile
    import zipfile

    env = os.environ.copy()
    temp_path_ = Path(temp_path)

    archive_dir = _ARCHIVE_DIR
    if config_settings:
        archive_dir_setting = config_settings.get("cmake.define.CMakePythonDistributions_ARCHIVE_DOWNLOAD_DIR")
        if isinstance(archive_dir_setting, list):
            archive_dir_setting = archive_dir_setting[-1]
        if archive_dir_setting:
            archive_dir = Path(archive_dir_setting)

    if os.name == "posix":
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
        kind = "unix_source"
    else:
        assert os.name == "nt"
        machine = platform.machine()
        kinds = {
            "x86": "win32_binary",
            "AMD64": "win64_binary",
            "ARM64": "winarm64_binary",
        }
        if machine not in kinds:
            msg = f"Could not find CMake required to build on a {machine} system"
            raise ValueError(msg)
        kind = kinds[machine]

    archive_path = _fetch_archive(kind, archive_dir)
    archive_name = archive_path.name

    if os.name == "posix":
        assert archive_name.endswith(".tar.gz")
        tar_filter_kwargs = {"filter": "tar"} if hasattr(tarfile, "tar_filter") else {}
        with tarfile.open(archive_path) as tar:
            tar.extractall(path=temp_path_, **tar_filter_kwargs)

        parallel_str = env.get("CMAKE_BUILD_PARALLEL_LEVEL", "1")
        parallel = max(0, int(parallel_str) if parallel_str.isdigit() else 1) or os.cpu_count() or 1

        bootstrap_path = next(temp_path_.glob("cmake-*/bootstrap"))
        prefix_path = temp_path_ / "cmake-install"
        cmake_path = prefix_path / "bin" / "cmake"
        bootstrap_args = [f"--prefix={prefix_path}", "--no-qt-gui", "--no-debugger", f"--parallel={parallel}", "--", "-DBUILD_TESTING=OFF", "-DBUILD_CursesDialog:BOOL=OFF"]
        for name in ("OPENSSL_ROOT_DIR", "OPENSSL_USE_STATIC_LIBS"):
            value = (config_settings or {}).get(f"cmake.define.{name}")
            if value is not None:
                bootstrap_args.append(f"-D{name}={value}")
        previous_cwd = Path().absolute()
        os.chdir(bootstrap_path.parent)
        try:
            subprocess.run([bootstrap_path, *bootstrap_args], env=env, check=True)
            subprocess.run([make_path, "-j", f"{parallel}"], env=env, check=True)
            subprocess.run([make_path, "install"], env=env, check=True)
        finally:
            os.chdir(previous_cwd)
    else:
        assert archive_name.endswith(".zip")
        with zipfile.ZipFile(archive_path) as zip_:
            zip_.extractall(path=temp_path_)
        cmake_path = next(temp_path_.glob("cmake-*/bin/cmake.exe"))

    return str(cmake_path)


def build_wheel(
    wheel_directory: str,
    config_settings: dict[str, list[str] | str] | None = None,
    metadata_directory: str | None = None,
) -> str:
    from scikit_build_core.errors import CMakeNotFoundError

    try:
        return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
    except CMakeNotFoundError:
        if os.name not in {"posix", "nt"}:
            raise
    # Let's try bootstrapping CMake
    import tempfile
    with tempfile.TemporaryDirectory() as temp_path:
        cmake_path = _bootstrap_build(temp_path, config_settings)
        assert cmake_path
        os.environ["CMAKE_EXECUTABLE"] = cmake_path
        return _orig.build_wheel(wheel_directory, config_settings, metadata_directory)
