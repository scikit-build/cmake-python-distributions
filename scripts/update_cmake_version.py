#!/usr/bin/env python3
#
# /// script
# dependencies = ["requests"]
# ///

"""
Command line executable allowing to update CMakeUrls.cmake given a CMake
version.
"""

from __future__ import annotations

import argparse
import contextlib
import re
import textwrap
from pathlib import Path

import requests

TYPE_CHECKING = False

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping


ROOT_DIR = Path(__file__).parent.parent.resolve()


@contextlib.contextmanager
def _log(txt: str, verbose: bool = True) -> Generator[None, None, None]:
    if verbose:
        print(txt)
    yield
    if verbose:
        print(f"{txt} - done")


def _major_minor(version: str) -> str:
    """Given a string of the form ``X.Y.Z``, returns ``X.Y``."""
    return ".".join(version.split(".")[:2])


def get_cmake_archive_urls_and_sha256s(version: str, verbose: bool=False) -> dict[str,tuple[str, str]]:
    files_base_url = (
        f"https://api.github.com/repos/Kitware/CMake/releases/tags/v{version}"
    )

    with _log(f"Collecting URLs and SHA256s from '{files_base_url}'"):

        assets = requests.get(files_base_url).json()["assets"]

        sha_256_file = f"cmake-{version}-SHA-256.txt"

        expected_files = {
            f"cmake-{version}.tar.gz": "unix_source",
            f"cmake-{version}.zip": "win_source",
            f"cmake-{version}-linux-x86_64.tar.gz": "linux64_binary",
            f"cmake-{version}-macos10.10-universal.tar.gz": "macos10_10_binary",
            f"cmake-{version}-windows-i386.zip": "win32_binary",
            f"cmake-{version}-windows-x86_64.zip": "win64_binary",
            f"cmake-{version}-windows-arm64.zip": "winarm64_binary",
        }

        # Get SHA256s for each asset
        shas = {}
        for asset in assets:
            if asset["name"] == sha_256_file:
                sha_256_url = asset["browser_download_url"]
                for line in requests.get(sha_256_url).text.splitlines():
                    file = line.split()[1].strip()
                    if file in expected_files:
                        sha256 = line.split()[0].strip()
                        identifier = expected_files[file]
                        shas[identifier] = sha256
        assert len(shas) == len(expected_files), f"{len(shas)} != {len(expected_files)}"

        # Get download URLs for each asset
        urls = {}
        for asset in assets:
            if asset["name"] in expected_files:
                identifier = expected_files[asset["name"]]
                urls[identifier] = asset["browser_download_url"]
        if len(urls) != len(expected_files):
            expected_files_by_identifier = {
                value: key for key, value in expected_files.items()
            }
            missing_files = []
            for identifier in set(expected_files.values()) - set(urls.keys()):
                missing_files.append(expected_files_by_identifier[identifier])
            raise RuntimeError(
                f"Couldn't find {missing_files} at {files_base_url}"
            )

        # combine the URLs and SHA256s into a single dictionary
        zipped = {}
        for value in expected_files.values():
            print(f"[{value}]\n{urls[value]}\n{shas[value]}\n")
            zipped[value] = (urls[value], shas[value])
        assert len(zipped) == len(expected_files)

        if verbose:
            for identifier, (url, sha256) in zipped.items():
                print(f"[{identifier}]\n{url}\n{sha256}\n")

        return zipped


def generate_cmake_variables(urls_and_sha256s: Mapping[str, tuple[str, str]]) -> str:
    template_inputs = {}

    # Get SHA256s and URLs
    for var_prefix, urls_and_sha256s_values in urls_and_sha256s.items():
        template_inputs[f"{var_prefix}_url"] = urls_and_sha256s_values[0]
        template_inputs[f"{var_prefix}_sha256"] = urls_and_sha256s_values[1]

    return textwrap.dedent(
        """
      #-----------------------------------------------------------------------------
      # CMake sources
      set(unix_source_url          "{unix_source_url}")
      set(unix_source_sha256       "{unix_source_sha256}")

      set(windows_source_url       "{win_source_url}")
      set(windows_source_sha256    "{win_source_sha256}")

      #-----------------------------------------------------------------------------
      # CMake binaries

      set(linux32_binary_url       "NA")  # Linux 32-bit binaries not available
      set(linux32_binary_sha256    "NA")

      set(linux64_binary_url       "{linux64_binary_url}")
      set(linux64_binary_sha256    "{linux64_binary_sha256}")

      set(macos10_10_binary_url    "{macos10_10_binary_url}")
      set(macos10_10_binary_sha256 "{macos10_10_binary_sha256}")

      set(win32_binary_url         "{win32_binary_url}")
      set(win32_binary_sha256      "{win32_binary_sha256}")

      set(win64_binary_url         "{win64_binary_url}")
      set(win64_binary_sha256      "{win64_binary_sha256}")

      set(winarm64_binary_url      "{winarm64_binary_url}")
      set(winarm64_binary_sha256   "{winarm64_binary_sha256}")
    """
    ).format(**template_inputs)


def update_cmake_urls_script(version: str) -> set[str]:
    content = generate_cmake_variables(get_cmake_archive_urls_and_sha256s(version))
    cmake_urls_filename = "CMakeUrls.cmake"
    cmake_urls_filepath = ROOT_DIR / cmake_urls_filename

    msg = f"Updating '{cmake_urls_filename}' with CMake version {version}"
    with _log(msg), cmake_urls_filepath.open("w") as cmake_file:
        cmake_file.write(content)

    return {cmake_urls_filename}


def _update_file(filepath: Path, regex: re.Pattern[str], replacement: str) -> None:
    with _log(f"Updating {filepath.relative_to(ROOT_DIR)}"):
        pattern = re.compile(regex)
        with filepath.open() as doc_file:
            updated_content = [pattern.sub(replacement, line) for line in doc_file]
        with filepath.open("w") as doc_file:
            doc_file.writelines(updated_content)


def update_docs(version: str) -> set[str]:
    pattern = re.compile(
        r"CMake \d.(\d)+.\d <https://cmake.org/cmake/help/v\d.(\d)+/index.html>"
    )
    replacement = f"CMake {version} <https://cmake.org/cmake/help/v{_major_minor(version)}/index.html>"
    files = {"docs/index.rst", "README.rst"}
    for filename in files:
        _update_file(ROOT_DIR / filename, pattern, replacement)
    return files


def update_tests(version: str) -> set[str]:
    pattern = re.compile(r'expected_version = "\d.\d+.\d"')
    replacement = f'expected_version = "{version}"'
    filename = "tests/test_cmake.py"
    _update_file(
        ROOT_DIR / filename, pattern, replacement
    )
    return {filename}


def update_pyproject_toml(version: str) -> set[str]:
    pattern = re.compile(r'^version = "[\w\.]+"$')
    replacement = f'version = "{version}"'
    filename = "pyproject.toml"
    _update_file(
        ROOT_DIR / filename, pattern, replacement
    )
    return {filename}


def update_raw_versions(version: str, filename: str) -> set[str]:
    pattern = re.compile(r"\d\.\d+\.\d")
    replacement = version
    _update_file(
        ROOT_DIR / filename, pattern, replacement
    )
    return {filename}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "cmake_version",
        metavar="CMAKE_VERSION",
        type=str,
        help="CMake version of the form X.Y.Z",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="If specified, only display the archive URLs and associated hashsums",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide the output",
    )
    args = parser.parse_args()

    if args.collect_only:
        get_cmake_archive_urls_and_sha256s(args.cmake_version, verbose=True)
        return

    filenames = set()
    filenames |= update_cmake_urls_script(args.cmake_version)
    filenames |= update_docs(args.cmake_version)
    filenames |= update_tests(args.cmake_version)
    filenames |= update_raw_versions(args.cmake_version, "docs/update_cmake_version.rst")
    filenames |= update_raw_versions(args.cmake_version, "docs/make_a_release.rst")
    filenames |= update_pyproject_toml(args.cmake_version)

    if args.quiet:
        return

    msg = f"""\
        Complete! Now run:

        git switch -c update-to-cmake-{args.cmake_version}
        git add -u {' '.join(filenames)}
        git commit -m "Update to CMake {args.cmake_version}"
        gh pr create --fill --body "Created by update_cmake_version.py"
        """
    print(textwrap.dedent(msg))


if __name__ == "__main__":
    main()
