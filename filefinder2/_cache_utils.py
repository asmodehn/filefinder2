import os
import sys

_PYCACHE = '__pycache__'

SOURCE_SUFFIXES = [b'.py']  # _setup() adds .pyw as needed.

DEBUG_BYTECODE_SUFFIXES = [b'.pyc']
OPTIMIZED_BYTECODE_SUFFIXES = [b'.pyo']

# Alternatives : (from hylang)
#     elif hasattr(imp, "cache_from_source"):
#         return imp.cache_from_source(source_path)
#     else:
#         # If source_path has a file extension, replace it with ".pyc".
#         # Otherwise, just append ".pyc".
#         d, f = os.path.split(source_path)
#         return os.path.join(d, re.sub(r"(?:\.[^.]+)?\Z", ".pyc", f))

def cache_from_source(path, debug_override=None):
    """Given the path to a .py file, return the path to its .pyc/.pyo file.

    The .py file does not need to exist; this simply returns the path to the
    .pyc/.pyo file calculated as if the .py file were imported.  The extension
    will be .pyc unless sys.flags.optimize is non-zero, then it will be .pyo.

    If debug_override is not None, then it must be a boolean and is used in
    place of sys.flags.optimize.

    If sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    debug = not sys.flags.optimize if debug_override is None else debug_override
    if debug:
        suffixes = DEBUG_BYTECODE_SUFFIXES
    else:
        suffixes = OPTIMIZED_BYTECODE_SUFFIXES
    head, tail = os.path.split(path)
    base_filename, sep, _ = tail.partition('.')
    tag = sys.implementation.cache_tag
    if tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    filename = ''.join([base_filename, sep, tag, suffixes[0]])
    return os.path.join(head, _PYCACHE, filename)


def source_from_cache(path):
    """Given the path to a .pyc./.pyo file, return the path to its .py file.

    The .pyc/.pyo file does not need to exist; this simply returns the path to
    the .py file calculated to correspond to the .pyc/.pyo file.  If path does
    not conform to PEP 3147 format, ValueError will be raised. If
    sys.implementation.cache_tag is None then NotImplementedError is raised.

    """
    if sys.implementation.cache_tag is None:
        raise NotImplementedError('sys.implementation.cache_tag is None')
    head, pycache_filename = os.path.split(path)
    head, pycache = os.path.split(head)
    if pycache != _PYCACHE:
        raise ValueError('{} not bottom-level directory in '
                         '{!r}'.format(_PYCACHE, path))
    if pycache_filename.count('.') != 2:
        raise ValueError('expected only 2 dots in '
                         '{!r}'.format(pycache_filename))
    base_filename = pycache_filename.partition('.')[0]
    return os.path.join(head, base_filename + SOURCE_SUFFIXES[0])
