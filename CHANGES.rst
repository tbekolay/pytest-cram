***************
Release History
***************

.. Changelog entries should follow this format:

   version (release date)
   ======================

   **section**

   - One-line description of change (link to Github issue/PR)

.. Changes should be organized in one of several sections:

   - Added
   - Changed
   - Deprecated
   - Removed
   - Fixed

0.2.2 (2020-08-08)
==================

**Fixed**

- Updated for recent pytest changes. (`#13`_)

.. _#13: https://github.com/tbekolay/pytest-cram/pull/13

0.2.1 (2020-05-10)
==================

**Fixed**

- Updated to use more recent pytest features. (`#11`_, `#12`_)

.. _#11: https://github.com/tbekolay/pytest-cram/pull/11
.. _#12: https://github.com/tbekolay/pytest-cram/pull/12

0.2.0 (2018-02-06)
==================

**Fixed**

- Fixed tests to work with ``pytest>=3.3``. Pytest added progress indicators
  to test output in version 3.3, which the tests were not expecting.

0.1.1 (2016-03-07)
==================

**Added**

- Added the ``--shell`` command line option and now checks the ``CRAMSHELL``
  environment variable to override the default ``/bin/sh`` shell. (`#3`_)

  Thanks to `Florian Rathgeber <https://github.com/kynan>`_ for the contribution!

**Changed**

- Depend explicitly on ``cram>=0.7``. If you would like support for earlier
  versions of cram, please
  `file an issue <https://github.com/tbekolay/pytest-cram/issues/new>`_.

.. _#3: https://github.com/tbekolay/pytest-cram/pull/3

0.1.0 (2016-02-28)
==================

Initial release of ``pytest-cram``! Supports Python 2.7+ and 3.3+.
