#!/usr/bin/env python3
#
# /// script
# dependencies = ["requests"]
# ///

"""
Command line executable allowing to update OpenSSL version.
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
    from collections.abc import Generator

ROOT_DIR = Path(__file__).parent.parent.resolve()


@contextlib.contextmanager
def _log(txt: str, verbose: bool=True) -> Generator[None, None, None]:
    if verbose:
        print(txt)
    yield
    if verbose:
        print(txt, "-", "done")


def get_openssl_sha256(version: str, verbose: bool=False) -> str:
    files_base_url = (
        f"https://www.openssl.org/source/openssl-{version}.tar.gz.sha256"
    )
    with _log(f"Collecting SHA256 from '{files_base_url}'"):
        sha256 = requests.get(files_base_url).content.decode("ascii").strip()
        if verbose:
            print("got sha256:", sha256)
        return sha256


def _update_file(filepath: Path, regex: re.Pattern[str], replacement: str) -> None:
    with _log(f"Updating {filepath.relative_to(ROOT_DIR)}"):
        pattern = re.compile(regex)
        with filepath.open() as doc_file:
            updated_content = [pattern.sub(replacement, line) for line in doc_file]
        with filepath.open("w") as doc_file:
            doc_file.writelines(updated_content)


def update_openssl_script(version: str, sha256: str) -> None:
    pattern = re.compile(r"^OPENSSL_ROOT=.*")
    replacement = f"OPENSSL_ROOT=openssl-{version}"
    _update_file(
        ROOT_DIR / "scripts/manylinux-build-and-install-openssl.sh", pattern, replacement
    )
    pattern = re.compile(r"^OPENSSL_HASH=.*")
    replacement = f"OPENSSL_HASH={sha256}"
    _update_file(
        ROOT_DIR / "scripts/manylinux-build-and-install-openssl.sh", pattern, replacement
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "openssl_version",
        metavar="OPENSSL_VERSION",
        type=str,
        help="OpenSSL version",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="If specified, only display the hashsum for the requested version",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Hide the output",
    )
    args = parser.parse_args()

    sha256 = get_openssl_sha256(args.openssl_version, verbose=args.collect_only)
    if args.collect_only:
        return

    update_openssl_script(args.openssl_version, sha256)

    if not args.quiet:
        msg = """\
            Complete! Now run:

            git switch -c update-to-openssl-{release}
            git add -u scripts/manylinux-build-and-install-openssl.sh
            git commit -m "Update to OpenSSL {release}"
            gh pr create --fill --body "Created by update_openssl_version.py"
            """
        print(textwrap.dedent(msg.format(release=args.openssl_version)))


if __name__ == "__main__":
    main()
