from __future__ import absolute_import, print_function


def print_importers():
    import sys
    import pprint

    print('PATH:'),
    pprint.pprint(sys.path)
    print()
    print('IMPORTERS:')
    for name, cache_value in sys.path_importer_cache.items():
        name = name.replace(sys.prefix, '...')
        print('{0!s}: {1!r}'.format(name, cache_value))
