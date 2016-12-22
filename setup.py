#!/usr/bin/env python

import sys
import versioneer

from pip.req import parse_requirements
from skbuild import setup


with open('README.rst', 'r') as fp:
    readme = fp.read()

with open('HISTORY.rst', 'r') as fp:
    history = fp.read().replace('.. :changelog:', '')


def _parse_requirements(filename):
    return [str(ir.req) for ir in parse_requirements(filename, session=False)]


requirements = []
dev_requirements = _parse_requirements('requirements-dev.txt')

# Require pytest-runner only when running tests
pytest_runner = (['pytest-runner>=2.0,<3dev']
                 if any(arg in sys.argv for arg in ('pytest', 'test'))
                 else [])

setup_requires = pytest_runner

setup(
    name='cmake',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    author='Jean-Christophe Fillion-Robin',
    author_email='jchris.fillionr@kitware.com',

    packages=['cmake'],

    cmake_install_dir='cmake/data',
    cmake_with_sdist=True,

    entry_points={
        'console_scripts': [
            'cmake=cmake:cmake', 'cpack=cmake:cpack', 'ctest=cmake:ctest'
        ]
    },

    url=r'http://cmake.org/',
    download_url=r'https://cmake.org/download',

    description=r'CMake is an open-source, cross-platform family of \
    tools designed to build, test and package software',

    long_description=readme + '\n\n' + history,

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

    install_requires=requirements,
    tests_require=dev_requirements,
    setup_requires=setup_requires
    )
