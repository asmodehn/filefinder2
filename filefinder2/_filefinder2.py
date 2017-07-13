from __future__ import absolute_import, division, print_function


"""
A module to find python file, but also embedding namespace package logic (PEP420)
"""

# We need to be extra careful with python versions
# Ref : https://docs.python.org/dev/library/importlib.html#importlib.import_module

import os
import sys

if (2, 7) <= sys.version_info < (3, 4):  # valid until which py3 version ?

    from ._utils import _verbose_message
    from ._fileloader2 import _ImportError, SourceFileLoader2, NamespaceLoader2, ImpLoader
    import imp
    import warnings

    class PathFinder2(object):
        """
        MetaFinder
        """

        @classmethod
        def invalidate_caches(cls):
            """Call the invalidate_caches() method on all path entry finders
            stored in sys.path_importer_caches (where implemented)."""
            for finder in sys.path_importer_cache.values():
                if hasattr(finder, 'invalidate_caches'):
                    finder.invalidate_caches()

        @classmethod
        def _path_hooks(cls, path):  # from importlib.PathFinder
            """Search sys.path_hooks for a finder for 'path'."""
            if sys.path_hooks is not None and not sys.path_hooks:
                warnings.warn('sys.path_hooks is empty', ImportWarning)
            for hook in sys.path_hooks:
                try:
                    return hook(path)
                except ImportError:
                    continue
            else:
                return None

        @classmethod
        def _path_importer_cache(cls, path):  # from importlib.PathFinder
            """Get the finder for the path entry from sys.path_importer_cache.
            If the path entry is not in the cache, find the appropriate finder
            and cache it. If no finder is available, store None.
            """
            if path == '':
                try:
                    path = os.getcwd()
                except FileNotFoundError:
                    # Don't cache the failure as the cwd can easily change to
                    # a valid directory later on.
                    return None
            try:
                finder = sys.path_importer_cache[path]
            except KeyError:
                finder = cls._path_hooks(path)
                sys.path_importer_cache[path] = finder

            return finder


    class NamespaceMetaFinder2(PathFinder2):
        """
        MetaFinder to handle Implicit (PEP 420) Namespace Packages
        """

        def __init__(self, *modules):
            """Initialisation of the finder depending on namespaces.
            The issue here is that we do not have enough information at this stage
            to determine which finder will be most appropriate for this path.

            Only after find_module might we known which one should be chosen."""
            self.module_names = modules

        @classmethod
        def find_module(cls, fullname, path=None):  # from importlib.PathFinder
            """Try to find the module on sys.path or 'path'
            The search is based on sys.path_hooks and sys.path_importer_cache.
            """
            if path is None:
                path = sys.path
            loader = None
            for entry in path:
                if not isinstance(entry, (str, bytes)):
                    continue
                finder = cls._path_importer_cache(entry)
                if finder is not None:
                    loader = finder.find_module(fullname)
                    if loader is not None:
                        break  # we stop at the first loader found

            # if no loader was found, we need to start the namespace finding logic
            if loader is None:
                for entry in path:
                    if not isinstance(entry, (str, bytes)):
                        continue
                    base_path = os.path.join(entry, fullname.rpartition('.')[-1])
                    if os.path.isdir(entry) and os.path.exists(base_path):  # this should now be considered a namespace
                        loader = NamespaceLoader2(fullname, base_path)
                    if loader is not None:
                        break  # we stop at the first loader found

            return loader


    class FileFinder2(object):
        """
        FileFinder to find modules and load them via Loaders for python 2.7
        """

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

            # We need to check that we will be able to find a module or package,
            # or raise ImportError to allow other finders to be instantiated for this path.
            # => the logic must correspond to find_module()
            findable = False
            for root, dirs, files in os.walk(self.path):
                findable = findable or any(
                    os.path.isfile(os.path.join(os.path.join(path, d), '__init__' + suffix))
                    for suffix, _ in self._loaders
                    for d in dirs
                ) or any(
                    f.endswith(suffix)
                    for suffix, _ in self._loaders
                    for f in files
                )

            if not findable:
                raise _ImportError("cannot find any matching module based on extensions {0}".format(
                    [s for s, _ in self._loaders]),
                    path=self.path
                )

        def find_module(self, fullname, path=None):
            """Try to find a loader for the specified module, or the namespace
            package portions. Returns loader."""
            path = path or self.path
            tail_module = fullname.rpartition('.')[2]

            base_path = os.path.join(path, tail_module)
            for suffix, loader_class in self._loaders:
                full_path = None  # adjusting path for package or file
                if os.path.isdir(base_path) and os.path.isfile(os.path.join(base_path, '__init__' + suffix)):
                    # __init__.py path will be computed by the loader when needed
                    return loader_class(fullname, base_path)
                elif os.path.isfile(base_path + suffix):
                    return loader_class(fullname, base_path + suffix)
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

    def get_supported_ns_loaders():
        """Returns a list of file-based module loaders.
        Each item is a tuple (loader, suffixes).
        """
        loaders = []
        for suffix, mode, type in imp.get_suffixes():
            if type == imp.PY_SOURCE:
                loaders.append((SourceFileLoader2, [suffix]))
            else:
                loaders.append((ImpLoader, [suffix]))
        return loaders

