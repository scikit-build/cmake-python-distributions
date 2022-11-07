.. _making_a_release:

================
Making a release
================

A core developer should use the following steps to create a release `X.Y.Z` of
**cmake-python-distributions** on `PyPI`_.

This is usually done after :ref:`updating_cmake_version`.

-------------
Prerequisites
-------------

* All CI tests are passing on `GitHub Actions`_.

* You have a `GPG signing key <https://help.github.com/articles/generating-a-new-gpg-key/>`_.

-------------------------
Documentation conventions
-------------------------

The commands reported below should be evaluated in the same terminal session.

Commands to evaluate starts with a dollar sign. For example::

  $ echo "Hello"
  Hello

means that ``echo "Hello"`` should be copied and evaluated in the terminal.



---------------------
`PyPI`_: Step-by-step
---------------------

1. Make sure that all CI tests are passing on `GitHub Actions`_.


2. Download the latest sources

  .. code::

    $ cd /tmp && \
      git clone git@github.com:scikit-build/cmake-python-distributions cmake-python-distributions-release && \
      cd cmake-python-distributions-release


3. List all tags sorted by version

  .. code::

    $ git fetch --tags && \
      git tag -l | sort -V


4. Choose the next release version number

  .. code::

    $ release=X.Y.Z

  .. warning::

      To ensure the packages are uploaded on `PyPI`_, tags must match this regular
      expression: ``^[0-9]+(\.[0-9]+)*(\.post[0-9]+)?$``.


5. Tag the release

  .. code::

    $ git tag --sign -m "cmake-python-distributions $release" $release master

  .. warning::

      We recommend using a `GPG signing key <https://help.github.com/articles/generating-a-new-gpg-key/>`_
      to sign the tag.


6. Publish the release tag

  .. code::

    $ git push origin $release

  .. note:: This will trigger builds on each CI services and automatically upload the wheels \
            and source distribution on `PyPI`_.

7. Check the status of the builds on `GitHub Actions`_.

8. Once the builds are completed, check that the distributions are available on `PyPI`_.

9. Make a GitHub release based on the tag. This will display the latest version
   in the GitHub sidebar, and will notify release watchers of the release.
   Title it `Version X.Y.Z` and add a little note about what changed (Python only).

10. Create a clean testing environment to test the installation

  .. code::

    $ pushd $(mktemp -d) && \
      mkvirtualenv cmake-$release-install-test && \
      pip install cmake && \
      cmake --version

  .. note::

      If the ``mkvirtualenv`` command is not available, this means you do not have `virtualenvwrapper`_
      installed, in that case, you could either install it or directly use `virtualenv`_ or `venv`_.

11. Cleanup

  .. code::

    $ popd && \
      deactivate  && \
      rm -rf dist/* && \
      rmvirtualenv cmake-$release-install-test


.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _virtualenv: http://virtualenv.readthedocs.io
.. _venv: https://docs.python.org/3/library/venv.html


.. _GitHub Actions: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml

.. _PyPI: https://pypi.org/project/cmake
