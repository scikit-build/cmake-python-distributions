# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

import nox

nox.options.sessions = ["lint", "build", "tests"]

BUILD_ENV = {
    "MACOSX_DEPLOYMENT_TARGET": "10.10",
}


built = ""


@nox.session
def build(session: nox.Session) -> str:
    """
    Make an SDist and a wheel. Only runs once.
    """
    global built
    if not built:
        session.log(
            "The files produced locally by this job are not intended to be redistributable"
        )
        session.install("build")
        tmpdir = session.create_tmp()
        session.run("python", "-m", "build", "--outdir", tmpdir, env=BUILD_ENV)
        (wheel_path,) = Path(tmpdir).glob("*.whl")
        (sdist_path,) = Path(tmpdir).glob("*.tar.gz")
        Path("dist").mkdir(exist_ok=True)
        wheel_path.rename(f"dist/{wheel_path.name}")
        sdist_path.rename(f"dist/{sdist_path.name}")
        built = wheel_path.name
    return built


@nox.session
def lint(session: nox.Session) -> str:
    """
    Run linters on the codebase.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session
def tests(session: nox.Session) -> str:
    """
    Run the tests.
    """
    wheel = build(session)
    session.install(f"./dist/{wheel}[test]")
    session.run("pytest", *session.posargs)


@nox.session
def docs(session: nox.Session) -> str:
    """
    Build the docs.
    """

    wheel = build(session)
    session.install("-r", "requirements-docs.txt")
    session.install(f"./dist/{wheel}")

    session.chdir("docs")
    session.run("sphinx-build", "-M", "html", ".", "_build")

    if session.posargs:
        if "serve" in session.posargs:
            print("Launching docs at http://localhost:8000/ - use Ctrl-C to quit")
            session.run("python", "-m", "http.server", "8000", "-d", "_build/html")
        else:
            print("Unsupported argument to docs")


def _bump(session: nox.Session, name: str, repository: str, branch: str, script: str, files) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--commit", action="store_true", help="Make a branch and commit."
    )
    parser.add_argument(
        "version", nargs="?", help="The version to process - leave off for latest."
    )
    args = parser.parse_args(session.posargs)

    if args.version is None:
        session.install("lastversion")
        lastversion_args = []
        if branch:
            lastversion_args.extend(("--branch", branch))
        lastversion_args.append(repository)
        version = session.run("lastversion", *lastversion_args, log=False, silent=True).strip()
    else:
        version = args.version

    session.install("requests")

    extra = ["--quiet"] if args.commit else []
    session.run("python", script, version, *extra)

    if args.commit:
        session.run("git", "switch", "-c", f"update-to-{name.lower()}-{version}", external=True)
        session.run("git", "add", "-u", *files, external=True)
        session.run("git", "commit", "-m", f"Update to {name} {version}", external=True)
        session.log(
            f'Complete! Now run: gh pr create --fill --body "Created by running `nox -s {session.name} -- --commit`"'
        )


@nox.session
def bump(session: nox.Session) -> None:
    """
    Set to a new version, use -- <version>, otherwise will use the latest version.
    """
    files = (
        "CMakeUrls.cmake",
        "docs/index.rst",
        "README.rst",
        "tests/test_cmake.py",
        "docs/update_cmake_version.rst",
    )
    _bump(session, "CMake", "kitware/cmake", "", "scripts/update_cmake_version.py", files)


@nox.session(name="bump-openssl")
def bump_openssl(session: nox.Session) -> None:
    """
    Set openssl to a new version, use -- <version>, otherwise will use the latest version.
    """
    files = (
        "scripts/manylinux-build-and-install-openssl.sh",
    )
    _bump(session, "OpenSSL", "openssl/openssl", "3.0", "scripts/update_openssl_version.py", files)
