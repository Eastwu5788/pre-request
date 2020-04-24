How to contribute to pre-request
====================================

Thank you for considering contributing to pre-request!

Prepare environment
----------------------

* Clone your Github fork locally

::

  git clone https://github.com/{yourname}/pre-request
  cd pre-request

* Add the main repository as a remote to update later

::

  git remote add pre-request  https://github.com/Eastwu5788/pre-request
  git fetch pre-request

* Create virtualenv

::

  python -m venv venv
  source ./venv/bin/active

* Install pre-request in editable mode with development dependencies:

::

  pip install -e ".[dev]"


* Install `pre-commit framework` and pre-commit hooks

::

  pip install pre-commit
  pre-commit install --install-hooks


Start coding
----------------

* Create a branch you would like to work on.

::

  git checkout -b your-branch-name origin/master


* Push your commits to Github and create a pull request by using

::

  git push --set-upstream origin your-branch-name


Running the tests
--------------------

Run the basic test suite with:

::

  pytest tests


Running test coverage
-----------------------

::

  coverage run -m pytest -p no:warnings
  coverage report -m


Building the docs
--------------------

Build the docs in the `docs` directory using Sphinx:

::

  cd docs
  pip install -r requirements.txt
  make html

Open `build/html/index.html` in your browser to view the docs.
