import pytest_cram

pytest_plugins = "pytester"


def test_version():
    assert pytest_cram.__version__


def test_cramignore(testdir):
    testdir.makeini("""
        [pytest]
        cramignore =
            sub/a*.t
            a.t
            c*.t
    """)
    testdir.tmpdir.ensure("sub/a.t")
    testdir.tmpdir.ensure("sub/a0.t")
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
        "a0.t s",
        "b.t s",
        "b0.t s",
        "*3 skipped*",
    ])
