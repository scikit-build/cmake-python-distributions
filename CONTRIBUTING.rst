============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

You can contribute in many ways:

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/scikit-build/cmake-python-distributions/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

The cmake-python-distributions project could always use more documentation. We welcome help
with the official cmake-python-distributions docs, in docstrings, or even on blog posts and
articles for the web.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at
https://github.com/scikit-build/cmake-python-distributions/issues.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)


Get Started
-----------

Ready to contribute? Here's how to set up `cmake-python-distributions` for local development.

1. Fork the `cmake-python-distributions` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/cmake-python-distributions.git

3. Install your local copy into a virtualenv. Assuming you have
   virtualenvwrapper installed (`pip install virtualenvwrapper`), this is how
   you set up your cloned fork for local development::

    $ mkvirtualenv cmake-python-distributions
    $ cd cmake-python-distributions/
    $ pip install -r requirements-dev.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and
   the tests::

    $ flake8
    $ python setup.py bdist_wheel
    $ python setup.py test

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.

2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in `README.rst`.

3. The pull request should work for Python 2.7, and 3.3, 3.4, 3.5.
   Check `AppVeyor <https://ci.appveyor.com/project/scikit-build/cmake-python-distributions-f3rbb>`_,
   `CircleCI <https://circleci.com/gh/scikit-build/cmake-python-distributions>`_
   and `TravisCi <https://travis-ci.org/scikit-build/cmake-python-distributions/pull_requests>`_
   and make sure that the tests pass for all supported Python versions.


Tips
----

To run a subset of tests::

	$ pytest tests/test_cmake.py
