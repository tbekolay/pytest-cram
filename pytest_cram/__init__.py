import os
import re

import cram
import pytest

from .compat import b
from .version import version as __version__


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption("--nocram", action="store_true",
                    help="do not run cram tests")
    group.addoption("--shell", default=os.environ.get('CRAMSHELL', '/bin/sh'),
                    help="shell to run cram tests with")
    parser.addini("cramignore", type="linelist",
                  help="each line specifies a file or file pattern that will "
                       "be ignored")


def pytest_collect_file(path, parent):
    config = parent.config
    ignored = any(path.fnmatch(ig) for ig in config.getini("cramignore"))

    if (not config.option.nocram
            and not ignored
            and path.ext == '.t'
            and path.basename[0] not in ('.', '_')):
        return CramItem(path, parent)


def pytest_configure(config):
    config.addinivalue_line("markers", "cram: mark test to execute using cram")


class CramError(Exception):
    """An error raised by cram."""


class CramItem(pytest.Item, pytest.File):
    """A cram test collected by pytest."""

    def __init__(self, path, parent):
        pytest.Item.__init__(self, path, parent)
        pytest.File.__init__(self, path, parent)
        self.add_marker("cram")
        tmpdir_factory = parent.config._tmpdirhandler
        name = re.sub("[\W]", "_", self.name)
        MAXVAL = 30
        if len(name) > MAXVAL:
            name = name[:MAXVAL]
        self.tmpdir = tmpdir_factory.mktemp(name, numbered=True)
        self.shell = parent.config.option.shell

    def runtest(self):
        with self.tmpdir.as_cwd():
            os.environ['CRAMTMP'] = str(self.tmpdir)
            ins, outs, diff = cram.testfile(b(str(self.fspath)),
                                            shell=self.shell)
        del os.environ['CRAMTMP']

        if outs is None and len(diff) == 0:
            pytest.skip("Process exited with return code 80")
        elif len(ins) == 0:
            pytest.skip("Test is empty")
        elif diff:
            raise CramError(diff)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(CramError):
            return b("").join(excinfo.value.args[0]).decode('ascii')
        return super(CramItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, None, "[cram] %s" % self.name
