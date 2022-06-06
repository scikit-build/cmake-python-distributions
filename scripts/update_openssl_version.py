#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line executable allowing to update OpenSSL version.
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


def get_openssl_sha256(version, verbose=False):
    files_base_url = (
        "https://www.openssl.org/source/openssl-%s.tar.gz.sha256" % version
    )
    with _log("Collecting SHA256 from '%s'" % files_base_url):
        sha256 = requests.get(files_base_url).content.decode("ascii").strip()
        if verbose:
            print("got sha256: {}".format(sha256))
        return sha256


def _update_file(filepath, regex, replacement):
    msg = "Updating %s" % os.path.relpath(filepath, ROOT_DIR)
    with _log(msg):
        pattern = re.compile(regex)
        with open(filepath, "r") as doc_file:
            lines = doc_file.readlines()
            updated_content = []
            for line in lines:
                updated_content.append(re.sub(pattern, replacement, line))
        with open(filepath, "w") as doc_file:
            doc_file.writelines(updated_content)


def update_openssl_script(version, sha256):
    pattern = re.compile(r"^OPENSSL_ROOT=.*")
    replacement = "OPENSSL_ROOT=openssl-%s" % version
    _update_file(
        os.path.join(ROOT_DIR, "scripts/manylinux-build-and-install-openssl.sh"), pattern, replacement
    )
    pattern = re.compile(r"^OPENSSL_HASH=.*")
    replacement = "OPENSSL_HASH=%s" % sha256
    _update_file(
        os.path.join(ROOT_DIR, "scripts/manylinux-build-and-install-openssl.sh"), pattern, replacement
    )


def main():
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
