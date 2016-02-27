.. image:: https://img.shields.io/pypi/v/pytest-cram.svg
  :target: https://pypi.python.org/pypi/pytest-cram
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pytest-cram.svg
  :target: https://pypi.python.org/pypi/pytest-cram
  :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/tbekolay/pytest-cram/master.svg
  :target: https://travis-ci.org/tbekolay/pytest-cram
  :alt: Travis-CI build status

.. image:: https://img.shields.io/coveralls/tbekolay/pytest-cram/master.svg
  :target: https://coveralls.io/r/tbekolay/pytest-cram?branch=master
  :alt: Test coverage


****************************************
pytest-cram: Run cram tests with py.test
****************************************

cram_ tests command line applications.
pytest_ tests Python applications.
pytest-cram tests Python command line applications
by letting you write your Python API tests with pytest,
and your command line tests in cram.
Best of both worlds!

.. _cram: https://bitheap.org/cram/
.. _pytest: http://pytest.org/latest/


Installation
============

To install and use pytest-cram, do::

  pip install pytest-cram

Nengo supports Python 2.6, 2.7, and 3.3+.

Usage
=====

Once installed, all ``.t`` files will be collected
and run with cram,
so installation should be all that is needed.
If you wish to disable cram tests for an invocation of
pytest, do::

  py.test --nocram

If you wish to disable specific cram tests,
list then in an ``.ini`` file like so::

  [pytest]
  cramignore = file1.t
      pattern*.t

..
   Documentation & Examples
   ========================

   Documentation can be found at ReadTheDocs
