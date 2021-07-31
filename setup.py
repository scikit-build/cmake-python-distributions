#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.text_file import TextFile

from skbuild import setup

# Add current folder to path
# This is required to import versioneer in an isolated pip build
# Prepending allows not to break on a non-isolated build when versioneer
# is already installed (c.f. https://github.com/scikit-build/cmake-python-distributions/issues/171)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import versioneer  # noqa: E402

with open('README.rst', 'r') as fp:
    readme = fp.read()

with open('HISTORY.rst', 'r') as fp:
    history = fp.read().replace('.. :changelog:', '')


def parse_requirements(filename):
    with open(filename, 'r') as file:
        return TextFile(filename, file).readlines()


test_requirements = parse_requirements('requirements-test.txt')

setup(
    name='cmake',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    author='Jean-Christophe Fillion-Robin',
    author_email='jchris.fillionr@kitware.com',

    package_dir={'': 'src'},
    packages=['cmake'],

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
        'Topic :: Software Development :: Build Tools'
        ],

    license='Apache 2.0',

    keywords='CMake build c++ fortran cross-platform cross-compilation',

    extras_require={"test": test_requirements},
)
