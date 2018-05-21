from __future__ import absolute_import, print_function

import pytest

def print_importers():
    """Helper function to print sys.path and importers cache"""
    import sys
    import pprint

    print('PATH:'),
    pprint.pprint(sys.path)
    print()
    print('IMPORTERS:')
    for name, cache_value in sys.path_importer_cache.items():
        name = name.replace(sys.prefix, '...')
        print('%s: %r' % (name, cache_value))


#: expect failure if we are in python2 and did NOT import filefinder2
xfail_py2_noff2 = pytest.mark.xfail(  # we need a string there to access the config at runtime
    "(pytest.config.getoption('--noff2')) and sys.version_info < (3, 4)",
    reason="python 2 does not support namespaces without importing filefinder2",
    strict=True
)

#: expect failure if we imported filefinder2 but did NOT activate it
xfail_py2_noactive = pytest.mark.xfail(  # we need a string there to access the config at runtime
    "(pytest.config.getoption('--noactive')) and sys.version_info < (3, 4)",
    reason="python 2 does not support namespaces without activating filefinder2",
    strict=True
)
