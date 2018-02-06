import os
import sys

import pytest

import pytest_cram

pytest_plugins = "pytester"


def test_version():
    assert pytest_cram.__version__


def test_nocram(testdir):
    """Ensure that --nocram collects .py but not .t files."""
    testdir.makefile('.t', "  $ true")
    testdir.makepyfile("def test_(): assert True")
    result = testdir.runpytest("--nocram")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_nocram.py .*", "*1 passed*"])


@pytest.mark.skipif(sys.platform == 'win32', reason="assuming Posix shell")
@pytest.mark.parametrize('shell', ['/bin/sh', '/bin/bash'])
def test_shell_cli(testdir, shell):
    """Ensure that --shell changes the shell used."""
    testdir.makefile('.t', r"""
        Echoing $0 should give us the current shell.

          $ echo "$0"
          {}
    """.format(shell))
    result = testdir.runpytest("--shell={}".format(shell))
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_shell_cli.t .*", "*1 passed*"])


@pytest.mark.skipif(sys.platform == 'win32', reason="assuming Posix shell")
@pytest.mark.parametrize('shell', ['/bin/sh', '/bin/bash'])
def test_shell_env(testdir, shell):
    """Ensure that the CRAMSHELL variable changes the shell used."""
    testdir.makefile('.t', r"""
        Echoing $0 should give us the current shell.

          $ echo "$0"
          {0}
          $ echo "$CRAMSHELL"
          {0}
    """.format(shell))
    os.environ["CRAMSHELL"] = shell
    result = testdir.runpytest()
    del os.environ["CRAMSHELL"]
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_shell_env.t .*", "*1 passed*"])


def test_cramignore(testdir):
    """Ensure that the cramignore option ignore the appropriate cram tests."""
    testdir.makeini("""
        [pytest]
        cramignore =
            sub/a*.t
            a.t
            c*.t
    """)
    testdir.tmpdir.ensure(os.path.join("sub", "a.t"))
    testdir.tmpdir.ensure(os.path.join("sub", "a0.t"))
    testdir.tmpdir.ensure("a.t")
    testdir.tmpdir.ensure("a0.t")
    testdir.tmpdir.ensure("b.t")
    testdir.tmpdir.ensure("b0.t")
    testdir.tmpdir.ensure("c.t")
    testdir.tmpdir.ensure("c0.t")

    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines([
        "*collected 3*",
        "a0.t s*",
        "b.t s*",
        "b0.t s*",
        "*3 skipped*",
    ])
