import os

pytest_plugins = "pytester"


def test_hidden(testdir):
    """Hidden examples. Should not be collected."""

    # Dealing with hidden paths, so easier with os.path.join
    p = str(testdir.tmpdir)
    with open(os.path.join(p, ".hidden.t"), 'w') as fp:
        fp.write("This test is ignored because it's hidden.\n")
    os.mkdir(os.path.join(p, ".hidden"))
    with open(os.path.join(p, ".hidden", "hidden.t"), 'w') as fp:
        fp.write("This test is ignored because it's hidden.\n")

    result = testdir.runpytest()
    assert result.ret != 0
    result.stdout.fnmatch_lines(["collected 0 items"])


def test_bare(testdir):
    """Bare example. Should pass."""
    testdir.makefile('.t', "  $ true")
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_bare.t .*", "*1 passed*"])


def test_empty(testdir):
    """Empty example. Should be skipped."""
    testdir.makefile('.t', "")
    result = testdir.runpytest("-rs")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_empty.t s*",
                                 "*Test is empty",
                                 "*1 skipped*"])
    result.stdout.fnmatch_lines(["test_empty.t s*", "*1 skipped*"])


def test_env(testdir):
    """Environment example. Should pass."""
    testdir.makefile('.t', r"""
        Check environment variables:

          $ echo "$LANG"
          C
          $ echo "$LC_ALL"
          C
          $ echo "$LANGUAGE"
          C
          $ echo "$TZ"
          GMT
          $ echo "$CDPATH"
  
          $ echo "$GREP_OPTIONS"
  
          $ echo "$CRAMTMP"
          .+ (re)
          $ echo "$TESTDIR"
          *{sep}test_env* (glob)
          $ ls "$TESTDIR"
          test_env.t
          $ echo "$TESTFILE"
          test_env.t
          $ pwd
          */test_env* (glob)
    """.format(sep=os.path.sep))
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_env.t .*", "*1 passed*"])


def test_fail(testdir):
    """Fail example. Should fail for several reasons."""
    testdir.makefile('.t', r"""
Output needing escaping:

  $ printf '\00\01\02\03\04\05\06\07\010\011\013\014\016\017\020\021\022\n'
  foo
  $ printf '\023\024\025\026\027\030\031\032\033\034\035\036\037\040\047\n'
  bar

Wrong output and bad regexes:

  $ echo 1
  2
  $ printf '1\nfoo\n1\n'
  +++ (re)
  foo\ (re)
   (re)

Filler to force a second diff hunk:


Offset regular expression:

  $ printf 'foo\n\n1\n'
  
  \d (re)
    """)

    # Subprocess needed for these weird shell commands
    result = testdir.runpytest()
    assert result.ret != 0
    result.stdout.fnmatch_lines(["test_fail.t F*",
                                 "@@ -1,18 +1,18 @@",
                                 r"+*\x11\x12 (esc)",
                                 r"*\x1e\x1f ' (esc)",
                                 "+  1",
                                 "@@ -20,5 +20,6 @@",
                                 "+  foo",
                                 "*1 failed*"])


def test_missingeol(testdir):
    """Missing EOL example. Should pass."""
    testdir.makefile('.t', "  $ printf foo", "  foo (no-eol)")
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_missingeol.t .*", "*1 passed*"])


def test_skip(testdir):
    """Skip example. Should be marked as skipped."""
    testdir.makefile('.t', """
        This test is considered "skipped" because it exits with return code
        80. This is useful for skipping tests that only work on certain
        platforms or in certain settings.

          $ exit 80
    """)
    result = testdir.runpytest("-rs")
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_skip.t s*",
                                 "*Process exited with return code 80",
                                 "*1 skipped*"])


def test_test(testdir):
    """Test example. Should pass."""
    testdir.makefile('.t', r"""
Simple commands:

  $ echo foo
  foo
  $ printf 'bar\nbaz\n' | cat
  bar
  baz

Multi-line command:

  $ foo() {
  >     echo bar
  > }
  $ foo
  bar

Regular expression:

  $ echo foobarbaz
  foobar.* (re)

Glob:

  $ printf '* \\foobarbaz {10}\n'
  \* \\fo?bar* {10} (glob)

Literal match ending in (re) and (glob):

  $ echo 'foo\Z\Z\Z bar (re)'
  foo\Z\Z\Z bar (re)
  $ echo 'baz??? quux (glob)'
  baz??? quux (glob)

Exit code:

  $ (exit 1)
  [1]

Write to stderr:

  $ echo foo >&2
  foo

No newline:

  $ printf foo
  foo (no-eol)
  $ printf 'foo\nbar'
  foo
  bar (no-eol)
  $ printf '  '
     (no-eol)
  $ printf '  \n  '
    
     (no-eol)
  $ echo foo
  foo
  $ printf foo
  foo (no-eol)

Escaped output:

  $ printf '\00\01\02\03\04\05\06\07\010\011\013\014\016\017\020\021\022\n'
  \x00\x01\x02\x03\x04\x05\x06\x07\x08\t\x0b\x0c\x0e\x0f\x10\x11\x12 (esc)
  $ printf '\023\024\025\026\027\030\031\032\033\034\035\036\037\040\047\n'
  \x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f ' (esc)
  $ echo hi
  \x68\x69 (esc)
  $ echo '(esc) in output (esc)'
  (esc) in output (esc)
  $ echo '(esc) in output (esc)'
  (esc) in output \x28esc\x29 (esc)

Command that closes a pipe:

  $ cat /dev/urandom | head -1 > /dev/null

If Cram let Python's SIGPIPE handler get inherited by this script, we
might see broken pipe messages.
    """)
    result = testdir.runpytest()
    assert result.ret == 0
    result.stdout.fnmatch_lines(["test_test.t .*", "*1 passed*"])
