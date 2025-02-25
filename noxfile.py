# /// script
# dependencies = ["nox>=2025.2.9"]
# ///

import argparse
import re
from pathlib import Path

import nox

nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv|virtualenv"

BUILD_ENV = {
    "MACOSX_DEPLOYMENT_TARGET": "10.10",
    "ARCHFLAGS": "-arch x86_64 -arch arm64",
}

wheel = ""


@nox.session
def build(session: nox.Session) -> str:
    """
    Make an SDist and a wheel.
    """
    session.log(
        "The files produced locally by this job are not intended to be redistributable"
    )
    extra = ["--installer=uv"] if session.venv_backend == "uv" else []
    session.install("build")
    tmpdir = session.create_tmp()
    session.run("python", "-m", "build", "--outdir", tmpdir, *extra, env=BUILD_ENV)
    (wheel_path,) = Path(tmpdir).glob("*.whl")
    (sdist_path,) = Path(tmpdir).glob("*.tar.gz")
    Path("dist").mkdir(exist_ok=True)
    wheel_path.rename(f"dist/{wheel_path.name}")
    sdist_path.rename(f"dist/{sdist_path.name}")

    global wheel
    wheel = f"dist/{wheel_path.name}"


@nox.session
def lint(session: nox.Session) -> str:
    """
    Run linters on the codebase.
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session(requires=["build"])
def tests(session: nox.Session) -> str:
    """
    Run the tests.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    deps = nox.project.dependency_groups(pyproject, "test")
    session.install(wheel, *deps)
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True, default=False)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "--non-interactive" to avoid serve. Pass "-- -b linkcheck" to check links.
    """
    pyproject = nox.project.load_toml("pyproject.toml")
    deps = nox.project.dependency_groups(pyproject, "docs")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", dest="builder", default="html", help="Build target (default: html)"
    )
    args, posargs = parser.parse_known_args(session.posargs)
    serve = args.builder == "html" and session.interactive

    extra_installs = ["sphinx-autobuild"] if serve else []
    session.install(*deps, *extra_installs)
    session.chdir("docs")

    if args.builder == "linkcheck":
        session.run(
            "sphinx-build", "-b", "linkcheck", ".", "_build/linkcheck", *posargs
        )
        return

    shared_args = (
        "-n",  # nitpicky mode
        "-T",  # full tracebacks
        f"-b={args.builder}",
        ".",
        f"_build/{args.builder}",
        *posargs,
    )

    if serve:
        session.run(
            "sphinx-autobuild", "--open-browser", "--ignore=.build", *shared_args
        )
    else:
        session.run("sphinx-build", "--keep-going", *shared_args)

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
        session.install("lastversion", "requests")
        lastversion_args = []
        if branch:
            lastversion_args.extend(("--branch", branch))
        lastversion_args.append(repository)
        version = session.run("lastversion", *lastversion_args, log=False, silent=True).strip()
    else:
        session.install("requests")
        version = args.version

    extra = ["--quiet"] if args.commit else []
    session.run("python", script, version, *extra)

    if args.commit:
        session.run("git", "switch", "-c", f"update-to-{name.lower()}-{version}", external=True)
        session.run("git", "add", "-u", *files, external=True)
        session.run("git", "commit", "-m", f"Update to {name} {version}", external=True)
        session.log(
            f'Complete! Now run: gh pr create --fill --body "Created by running `nox -s {session.name} -- --commit`"'
        )


@nox.session(default=False)
def bump(session: nox.Session) -> None:
    """
    Set to a new version, use -- <version>, otherwise will use the latest version.
    """
    files = (
        "pyproject.toml",
        "CMakeUrls.cmake",
        "docs/index.rst",
        "README.rst",
        "tests/test_cmake.py",
        "docs/update_cmake_version.rst",
    )
    _bump(session, "CMake", "kitware/cmake", "", "scripts/update_cmake_version.py", files)


@nox.session(name="bump-openssl", default=False)
def bump_openssl(session: nox.Session) -> None:
    """
    Set openssl to a new version, use -- <version>, otherwise will use the latest version.
    """
    files = (
        "scripts/manylinux-build-and-install-openssl.sh",
    )
    _bump(session, "OpenSSL", "openssl/openssl", "3.0", "scripts/update_openssl_version.py", files)


def _get_version() -> str:
    txt = Path("pyproject.toml").read_text()
    return next(iter(re.finditer(r'^version = "([\d\.]+)"$', txt, flags=re.MULTILINE))).group(1)


@nox.session(venv_backend="none", default=False)
def tag_release(session: nox.Session) -> None:
    """
    Print instructions for tagging a release and pushing it to GitHub.
    """

    session.log("Run the following commands to make a release:")
    current_version = _get_version()
    print(f"git tag --sign -m 'cmake-python-distributions {current_version}' {current_version} main")
    print(f"git push origin {current_version}")


@nox.session(venv_backend="none", default=False)
def cmake_version(session: nox.Session) -> None:  # noqa: ARG001
    """
    Print upstream cmake version.
    """

    current_version = _get_version()
    print(".".join(current_version.split(".")[:3]))


@nox.session(venv_backend="none", default=False)
def openssl_version(session: nox.Session) -> None:  # noqa: ARG001
    """
    Print upstream OpenSSL version.
    """
    txt = Path("scripts/manylinux-build-and-install-openssl.sh").read_text()
    current_version = next(iter(re.finditer(r'^OPENSSL_ROOT=openssl-([\d\.]+)$', txt, flags=re.MULTILINE))).group(1)
    print(".".join(current_version.split(".")[:3]))
