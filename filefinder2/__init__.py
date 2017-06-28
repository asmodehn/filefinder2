from __future__ import absolute_import, print_function

import sys

# Selective Import here to allow extending the import logic with other py2.7 importers
if (2, 7) <= sys.version_info < (3, 4):  # TODO : test : valid until which py3 version ?
    from ._filefinder2 import get_supported_ns_loaders, FileFinder2, FileLoader2


# Making the activation explicit for now
def activate():
    """Install the path-based import components."""
    if (2, 7) <= sys.version_info < (3, 4):  # TODO : test : valid until which py3 version ?
        supported_loaders = get_supported_ns_loaders()
        ns_hook = FileFinder2.path_hook(*supported_loaders)
        # Note this must be early in the list, since we change the logic regarding what is a package or not
        sys.path_hooks.insert(1, ns_hook)
        # Resetting sys.path_importer_cache values that are set to None (using default),
        # to support the case where we have an implicit package inside an already loaded package,
        # since we need to replace the default importer.
        for path in [p for p, i in sys.path_importer_cache.items() if i is None]:
            sys.path_importer_cache.pop(path)
    else:
        # Useful to avoid traps since logic is different with finder and loader on python3
        raise ImportError("filefinder2 : Unsupported python version")
