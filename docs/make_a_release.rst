=====================
How to Make a Release
=====================

A core developer should use the following steps to create a release of
**cmake-python-distributions**.

0. Configure `~/.pypirc` as described `here <https://packaging.python.org/distributing/#uploading-your-project-to-pypi>`_.

1. Make sure that all CI tests are passing: `AppVeyor <https://ci.appveyor.com/project/scikit-build/cmake-python-distributions-f3rbb>`_,
   `CircleCI <https://circleci.com/gh/scikit-build/cmake-python-distributions>`_
   and `TravisCi <https://travis-ci.org/scikit-build/cmake-python-distributions/pull_requests>`_.

2. Tag the release. Requires a GPG key with signatures. For version *X.Y.Z*::

    release=X.Y.Z
    git tag -s -m "cmake-python-distributions ${release}" ${release} origin/master

3. Clear the content of `dist <https://data.kitware.com/#collection/5817c33a8d777f10f26ee3a7/folder/5817c83c8d777f10f26ee3ab>`_ folder
   associated with the collection `CMake Python Distributions` hosted on https://data.kitware.com.

4. Push the tag::

    git push origin ${release}

5. If needed, explicitly trigger a build on each CI services, and wait for all wheels and source
   distribution to be uploaded into the `dist <https://data.kitware.com/#collection/5817c33a8d777f10f26ee3a7/folder/5817c83c8d777f10f26ee3ab>`_
   folder.

6. Download locally the source distribution and all the wheels::

    rm -rf ./dist/
    pip install girder-client
    girder-cli --api-key API_KEY  \
      --api-url https://data.kitware.com/api/v1 download \
      --parent-type folder 5817c83c8d777f10f26ee3ab ./dist/


4. Upload the packages to the testing PyPI instance::

    pip install -U twine
    twine upload --sign -r pypitest dist/*

5. Check the `PyPI testing package page <https://test.pypi.org/project/cmake/>`_.

6. Upload the packages to the PyPI instance::

    twine upload --sign dist/*

7. Check the `PyPI package page <https://pypi.org/project/cmake/>`_.

8. Make sure the package can be installed::

    mkvirtualenv test-pip-install
    pip install cmake
    cmake --version
    rmvirtualenv test-pip-install
