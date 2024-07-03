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


---------------------
`PyPI`_: Step-by-step
---------------------

1. Make sure that all CI tests are passing on `GitHub Actions`_.


2. Download the latest sources if you don't already have them

  .. code:: console

    $ git clone git@github.com:scikit-build/cmake-python-distributions
    $ cd cmake-python-distributions


3. Ask nox for the instructions on what to type

  .. code:: console

    $ nox -s tag_release


4. Run the suggested lines, probably something like this:

  .. code:: console

    $ git tag --sign -m 'cmake-python-distributions 3.30.0' 3.30.0 main
    $ git push origin 3.30.0

  .. warning::

      We recommend using a `GPG signing key <https://help.github.com/articles/generating-a-new-gpg-key/>`_
      to sign the tag.


5. Check the status of the builds on `GitHub Actions`_.

6. Once the builds are completed, check that the distributions are available on `PyPI`_.

7. Make a GitHub release based on the tag. This will display the latest version
   in the GitHub sidebar, and will notify release watchers of the release.
   Title it `Version X.Y.Z` and add a little note about what changed (Python only).


.. _GitHub Actions: https://github.com/scikit-build/cmake-python-distributions/actions/workflows/build.yml

.. _PyPI: https://pypi.org/project/cmake
