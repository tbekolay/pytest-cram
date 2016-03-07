"""Deal with different Python and cram versions"""

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

bytestype = getattr(builtins, 'bytes', str)

if bytestype is str:

    def b(s):
        return s

else:

    def b(s):
        return s.encode('ascii')
