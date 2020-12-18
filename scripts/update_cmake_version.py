"""Command line executable allowing to update CMakeUrls.cmake
 given a CMake version.
"""

import argparse
import contextlib
import os
import re
import textwrap

try:
    import requests
except ImportError:
    raise SystemExit(
        "requests not available: "
        "consider installing it running 'pip install requests'"
    )

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")


@contextlib.contextmanager
def _log(txt, verbose=True):
    if verbose:
        print(txt)
    yield
    if verbose:
        print("%s - done" % txt)


def _major_minor(version):
    """Given a string of the form ``X.Y.Z``, returns ``X.Y``."""
    return ".".join(version.split(".")[:2])


def get_cmake_archive_urls_and_sha256s(version, verbose=False):
    files_base_url = "https://api.github.com/repos/Kitware/CMake/releases/tags/v%s" % version

    with _log("Collecting URLs and SHA256s from '%s'" % files_base_url):

        assets = requests.get(files_base_url).json()['assets']

        sha_256_file = "cmake-%s-SHA-256.txt" % version

        expected_files = {
            "cmake-%s.tar.gz" % version:               "unix_source",
            "cmake-%s.zip" % version:                  "win_source",
            "cmake-%s-Linux-x86_64.tar.gz" % version:  "linux64_binary",
            "cmake-%s-Darwin-x86_64.tar.gz" % version: "macosx_binary",
            "cmake-%s-win32-x86.zip" % version:        "win32_binary",
            "cmake-%s-win64-x64.zip" % version:        "win64_binary",
        }

        # Get SHA256s for each asset
        shas = {}
        for asset in assets:
            if asset['name'] == sha_256_file:
                sha_256_url = asset['browser_download_url']
                for line in requests.get(sha_256_url).text.splitlines():
                    file = line.split()[1].strip()
                    if file in expected_files:
                        sha256 = line.split()[0].strip()
                        identifier = expected_files[file]
                        shas[identifier] = sha256
        assert len(shas) == len(expected_files), "{} != {}".format(len(shas), len(expected_files))

        # Get download URLs for each asset
        urls = {}
        for asset in assets:
            if asset['name'] in expected_files:
                identifier = expected_files[asset['name']]
                urls[identifier] = asset['browser_download_url']
        if len(urls) != len(expected_files):
            expected_files_by_identifier = {value: key for key, value in expected_files.items()}
            missing_files = []
            for identifier in set(expected_files.values()) - set(urls.keys()):
                missing_files.append(expected_files_by_identifier[identifier])
            raise RuntimeError("Couldn't find %s at %s" % (missing_files, files_base_url))

        # combine the URLs and SHA256s into a single dictionary
        zipped = {}
        for value in expected_files.values():
            print("[%s]\n%s\n%s\n" % (value, urls[value], shas[value]))
            zipped[value] = (urls[value], shas[value])
        assert len(zipped) == len(expected_files)

        if verbose:
            for identifier, (url, sha256) in zipped.items():
                print("[%s]\n%s\n%s\n" % (identifier, url, sha256))

        return zipped


def generate_cmake_variables(urls_and_sha256s):
    template_inputs = {}

    # Get SHA256s and URLs
    for var_prefix, urls_and_sha256s in urls_and_sha256s.items():
        template_inputs["%s_url" % var_prefix] = urls_and_sha256s[0]
        template_inputs["%s_sha256" % var_prefix] = urls_and_sha256s[1]

    cmake_variables = textwrap.dedent("""
      #-----------------------------------------------------------------------------
      # CMake sources
      set(unix_source_url       "{unix_source_url}")
      set(unix_source_sha256    "{unix_source_sha256}")

      set(windows_source_url    "{win_source_url}")
      set(windows_source_sha256 "{win_source_sha256}")

      #-----------------------------------------------------------------------------
      # CMake binaries

      set(linux32_binary_url    "NA")  # Linux 32-bit binaries not available
      set(linux32_binary_sha256 "NA")

      set(linux64_binary_url    "{linux64_binary_url}")
      set(linux64_binary_sha256 "{linux64_binary_sha256}")

      set(macosx_binary_url    "{macosx_binary_url}")
      set(macosx_binary_sha256 "{macosx_binary_sha256}")

      set(win32_binary_url    "{win32_binary_url}")
      set(win32_binary_sha256 "{win32_binary_sha256}")

      set(win64_binary_url    "{win64_binary_url}")
      set(win64_binary_sha256 "{win64_binary_sha256}")
    """).format(**template_inputs)

    return cmake_variables


def update_cmake_urls_script(version):
    content = generate_cmake_variables(
        get_cmake_archive_urls_and_sha256s(version))
    cmake_urls_filename = "CMakeUrls.cmake"
    cmake_urls_filepath = os.path.join(ROOT_DIR, cmake_urls_filename)

    msg = "Updating '%s' with CMake version %s" % (cmake_urls_filename, version)
    with _log(msg), open(cmake_urls_filepath, "w") as cmake_file:
        cmake_file.write(content)


def _update_file(filepath, regex, replacement):
    msg = "Updating %s" % os.path.relpath(filepath, ROOT_DIR)
    with _log(msg):
        pattern = re.compile(regex)
        with open(filepath, 'r') as doc_file:
            lines = doc_file.readlines()
            updated_content = []
            for line in lines:
                updated_content.append(
                    re.sub(pattern, replacement, line))
        with open(filepath, "w") as doc_file:
            doc_file.writelines(updated_content)


def update_docs(version):
    pattern = re.compile(
        r"CMake \d.(\d)+.\d <https://cmake.org/cmake/help/v\d.(\d)+/index.html>")
    replacement = (
        "CMake %s <https://cmake.org/cmake/help/v%s/index.html>" % (
            version, _major_minor(version)))
    for filename in ["docs/index.rst", "README.rst"]:
        _update_file(os.path.join(ROOT_DIR, filename), pattern, replacement)


def update_tests(version):
    pattern = re.compile(r'expected_version = "\d.(\d)+.\d"')
    replacement = 'expected_version = "%s"' % version
    _update_file(os.path.join(
        ROOT_DIR, "tests/test_distribution.py"), pattern, replacement)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'cmake_version', metavar='CMAKE_VERSION', type=str,
        help='CMake version of the form X.Y.Z'
    )
    parser.add_argument(
        '--collect-only', action='store_true',
        help='If specified, only display the archive URLs and associated hashsums'
    )
    args = parser.parse_args()
    if args.collect_only:
        get_cmake_archive_urls_and_sha256s(args.cmake_version, verbose=True)
    else:
        update_cmake_urls_script(args.cmake_version)
        update_docs(args.cmake_version)
        update_tests(args.cmake_version)


if __name__ == "__main__":
    main()
