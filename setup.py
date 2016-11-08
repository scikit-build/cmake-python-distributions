#!/usr/bin/env python

import versioneer

from pip.req import parse_requirements
from skbuild import setup


def _parse_requirements(filename):
    return [str(ir.req) for ir in parse_requirements(filename, session=False)]

dev_requirements = _parse_requirements('requirements-dev.txt')

setup(
    name='cmake',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    author='Jean-Christophe Fillion-Robin',
    author_email='jchris.fillionr@kitware.com',

    packages=['cmake'],

    cmake_install_dir='cmake/data',

    entry_points={
        'console_scripts': [
            'cmake=cmake:cmake', 'cpack=cmake:cpack', 'ctest=cmake:ctest'
        ]
    },

    url=r'http://cmake.org/',
    download_url=r'https://cmake.org/download',

    description=r'CMake is an open-source, cross-platform family of \
    tools designed to build, test and package software',

    long_description='CMake is used to control the software compilation  \
    process using simple platform and compiler independent configuration \
    files, and generate native makefiles and workspaces that can be used \
    in the compiler environment of your choice. The suite of CMake tools \
    were created by Kitware in response to the need for a powerful,      \
    cross-platform build environment for open-source projects such as    \
    ITK and VTK.',

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
        'Topic :: Software Development :: Build Tools'
        ],

    license='Apache 2.0',

    keywords='CMake build c++ fortran cross-platform cross-compilation',

    install_requires=[],
    tests_require=dev_requirements,
    )
