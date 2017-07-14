from __future__ import absolute_import, print_function

import sys

# Selective Import here to allow extending the import logic with other py2.7 importers
if (2, 7) <= sys.version_info < (3, 4):  # TODO : test : valid until which py3 version ?
    from ._filefinder2 import get_supported_ns_loaders, PathFinder2, NamespaceMetaFinder2, FileFinder2
    from ._fileloader2 import NamespaceLoader2, Loader2, SourceFileLoader2, ImpLoader

    supported_loaders = get_supported_ns_loaders()
    path_hook = FileFinder2.path_hook(*supported_loaders)


# Making the activation explicit for now
def activate():
    """Install the path-based import components."""
    if (2, 7) <= sys.version_info < (3, 4):  # TODO : test : valid until which py3 version ?
        if path_hook not in sys.path_hooks:
            sys.path_hooks.append(path_hook)
        # Resetting sys.path_importer_cache values,
        # to support the case where we have an implicit package inside an already loaded package,
        # since we need to replace the default importer.
        sys.path_importer_cache.clear()

        if NamespaceMetaFinder2 not in sys.meta_path:
            # Setting up the meta_path to change package finding logic
            sys.meta_path.append(NamespaceMetaFinder2)

    else:
        # Useful to avoid traps since logic is likely different with finder and loader on python3
        raise ImportError("filefinder2 : Unsupported python version")
