#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.text_file import TextFile

from skbuild import setup

with open('README.rst', 'r') as fp:
    readme = fp.read()

with open('HISTORY.rst', 'r') as fp:
    history = fp.read().replace('.. :changelog:', '')


def parse_requirements(filename):
    with open(filename, 'r') as file:
        return TextFile(filename, file).readlines()


test_requirements = parse_requirements('requirements-test.txt')

try:
    setup(
        name='cmake',

        author='Jean-Christophe Fillion-Robin',
        author_email='jchris.fillionr@kitware.com',

        package_dir={'': 'src'},
        packages=['cmake'],
        package_data={"cmake": ["py.typed"]},

        cmake_install_dir='src/cmake/data',

        entry_points={
            'console_scripts': [
                'cmake=cmake:cmake', 'cpack=cmake:cpack', 'ctest=cmake:ctest'
            ]
        },

        url='https://cmake.org/',
        download_url='https://cmake.org/download',
        project_urls={
            "Documentation": "https://cmake-python-distributions.readthedocs.io/",
            "Source Code": "https://github.com/scikit-build/cmake-python-distributions",
            "Mailing list": "https://groups.google.com/forum/#!forum/scikit-build",
            "Bug Tracker": "https://github.com/scikit-build/cmake-python-distributions/issues",
        },


        description='CMake is an open-source, cross-platform family of '
                    'tools designed to build, test and package software',

        long_description=readme + '\n\n' + history,
        long_description_content_type='text/x-rst',

        classifiers=[
            'License :: OSI Approved :: Apache Software License',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: C',
            'Programming Language :: C++',
            'Programming Language :: Fortran',
            'Programming Language :: Python',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'Typing :: Typed',
        ],

        license='Apache 2.0',

        keywords='CMake build c++ fortran cross-platform cross-compilation',

        extras_require={"test": test_requirements},
    )
except BaseException:
    # Note: This is a bare exception that re-raises so that we don't interfere
    # with anything the installation machinery might want to do. Because we
    # print this for any exception this msg can appear (e.g. in verbose logs)
    # even if there's no failure. For example, SetupRequirementsError is raised
    # during PEP517 building and prints this text. setuptools raises SystemExit
    # when compilation fails right now, but it's possible this isn't stable
    # or a public API commitment so we'll remain ultra conservative.
    import platform
    import subprocess
    try:
        import pkg_resources
    except ImportError:
        pass

    print(
        """
    =============================DEBUG ASSISTANCE=============================
    If you are seeing a compilation error please try the following steps to
    successfully install cmake:
    1) Upgrade to the latest pip and try again. This will fix errors for most
       users. See: https://pip.pypa.io/en/stable/installing/#upgrading-pip
    2) If running on Raspberry Pi OS, you can set PIP_ONLY_BINARY=cmake in
       order to retrieve the latest wheels built by piwheels.
       c.f. https://github.com/scikit-build/cmake-python-distributions/issues/392#issuecomment-1676284749
    3) If on Linux, with glibc < 2.12, you can set PIP_ONLY_BINARY=cmake in
       order to retrieve the last manylinux1 compatible wheel.
    4) If on Linux, with glibc < 2.12, you can cap "cmake<3.23" in your
       requirements in order to retrieve the last manylinux1 compatible wheel.
    5) Open an issue with the debug information that follows at
       https://github.com/scikit-build/cmake-python-distributions/issues
    """
    )
    print("    Python: %s" % '.'.join(str(v) for v in sys.version_info[:3]))
    print("    platform: %s" % platform.platform())
    if sys.platform.startswith("linux"):
        try:
            print("    glibc: %s" % os.confstr("CS_GNU_LIBC_VERSION"))
        except BaseException:
            try:
                import ctypes
                process_namespace = ctypes.CDLL(None)
                gnu_get_libc_version = process_namespace.gnu_get_libc_version
                gnu_get_libc_version.restype = ctypes.c_char_p
                glibc_version = gnu_get_libc_version()
                if not isinstance(glibc_version, str):
                    glibc_version = glibc_version.decode("ascii")
                    print("    glibc: %s" % glibc_version)
            except BaseException:
                pass
    if sys.platform.startswith("darwin"):
        try:
            macos_ver = subprocess.check_output(
                [
                    sys.executable,
                    "-sS",
                    "-c",
                    "import platform; print(platform.mac_ver()[0])",
                ],
                universal_newlines=True,
                env={"SYSTEM_VERSION_COMPAT": "0"},
            ).strip()
            print("    macos: %s" % macos_ver)
        except BaseException:
            try:
                print("    macos: %s" % platform.mac_ver()[0])
            except BaseException:
                pass
    print("    machine: %s" % platform.machine())
    print("    bits: %d" % (64 if sys.maxsize > 2**32 else 32))
    for dist in ["pip", "setuptools", "scikit-build"]:
        try:
            version = pkg_resources.get_distribution(dist).version
        except BaseException:
            version = "n/a"
        print("    {}: {}".format(dist, version))
    for key in ["PEP517_BUILD_BACKEND"]:
        if key in os.environ:
            print("    {}={}".format(key, os.environ[key]))
    print(
        """\
    =============================DEBUG ASSISTANCE=============================
    """
    )
    raise
