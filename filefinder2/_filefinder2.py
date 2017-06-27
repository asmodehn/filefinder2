from __future__ import absolute_import, division, print_function


"""
A module to find python file, but also embedding namespace package logic (PEP420), implemented via pkg_resources
"""

# We need to be extra careful with python versions
# Ref : https://docs.python.org/dev/library/importlib.html#importlib.import_module

import os
import sys

if (2, 7) <= sys.version_info < (3, 4):  # valid until which py3 version ?

    from ._utils import _verbose_message
    from ._fileloader2 import _ImportError, FileLoader2
    import imp

    class FileFinder2(object):
        def __init__(self, path, *loader_details):
            """Initialize with the path to search on and a variable number of
            2-tuples containing the loader and the file suffixes the loader
            recognizes."""
            loaders = []
            for loader, suffixes in loader_details:
                loaders.extend((suffix, loader) for suffix in suffixes)
            self._loaders = loaders
            # Base (directory) path
            self.path = path or '.'
            # Note : we are not playing with cache here (too complex to get right and not worth it for obsolete python)

        def find_module(self, fullname, path=None):
            """Try to find a loader for the specified module, or the namespace
            package portions. Returns loader."""
            path = path or self.path
            tail_module = fullname.rpartition('.')[2]

            base_path = os.path.join(path, tail_module)
            for suffix, loader_class in self._loaders:
                full_path = None  # adjusting path for package or file
                if os.path.isdir(base_path) and os.path.isfile(os.path.join(base_path, '__init__' + suffix)):
                    return loader_class(fullname, base_path)  # __init__.py path will be computed by the loader when needed
                elif os.path.isfile(base_path + suffix):
                    return loader_class(fullname, base_path + suffix)
            else:
                if os.path.isdir(base_path):
                    # If a namespace package, return the path if we don't
                    #  find a module in the next section.
                    _verbose_message('possible namespace for {}'.format(base_path))
                    return FileLoader2(fullname, base_path)

            return None

        @classmethod
        def path_hook(cls, *loader_details):
            """A class method which returns a closure to use on sys.path_hook
            which will return an instance using the specified loaders and the path
            called on the closure.

            If the path called on the closure is not a directory, ImportError is
            raised.

            """
            def path_hook_for_FileFinder2(path):
                """Path hook for FileFinder2."""
                if not os.path.isdir(path):
                    raise _ImportError('only directories are supported', path=path)
                return cls(path, *loader_details)

            return path_hook_for_FileFinder2

        def __repr__(self):
            return 'FileFinder2({!r})'.format(self.path)

    def _get_supported_ns_loaders():
        """Returns a list of file-based module loaders.
        Each item is a tuple (loader, suffixes).
        """
        loader = FileLoader2, [suffix for suffix, mode, type in imp.get_suffixes()]
        return [loader]


def _install_hook():
    """Install the path-based import components."""
    if (2, 7) <= sys.version_info < (3, 4):  # TODO : test : valid until which py3 version ?
        supported_loaders = _get_supported_ns_loaders()
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

