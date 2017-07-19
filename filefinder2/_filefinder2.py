from __future__ import absolute_import, division, print_function

import collections

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

    # to be compatible with py3 importlib
    SourcelessFileLoader2 = ImpLoader
    ExtensionFileLoader2 = ImpLoader

    def get_supported_file_loaders():
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

    # Implementing a quick Module spec, ported from python3
    # to provide a py2/py3 API
    class ModuleSpec:
        def __init__(self, name, loader, origin=None, loader_state=None, is_package=None):
            self.name = name
            self.loader = loader
            self.origin = origin
            self.loader_state = loader_state
            self.submodule_search_locations = [] if is_package else None

    # Implementing spec_from_file_location, ported from python3
    # to provide a py2/py3 API
    def spec_from_file_location(name, location=None, loader=None, submodule_search_locations=None):
        """Return a module spec based on a file location.
        To indicate that the module is a package, set
        submodule_search_locations to a list of directory paths.  An
        empty list is sufficient, though its not otherwise useful to the
        import system.
        """
        if location is None:
            # The caller may simply want a partially populated location-
            # oriented spec.  So we set the location to a bogus value and
            # fill in as much as we can.
            location = '<unknown>'
            if hasattr(loader, 'get_filename'):
                # ExecutionLoader
                try:
                    location = loader.get_filename(name)
                except ImportError:
                    pass

        # If the location is on the filesystem, but doesn't actually exist,
        # we could return None here, indicating that the location is not
        # valid.  However, we don't have a good way of testing since an
        # indirect location (e.g. a zip file or URL) will look like a
        # non-existent file relative to the filesystem.

        spec = ModuleSpec(name, loader, origin=location)

        # Pick a loader if one wasn't provided.
        if loader is None:
            for loader_class, suffixes in get_supported_file_loaders():
                if location.endswith(tuple(suffixes)):
                    loader = loader_class(name, location)
                    spec.loader = loader
                    break
            else:
                return None

        # Set submodule_search_paths appropriately.
        if submodule_search_locations is None:
            # Check the loader.
            if hasattr(loader, 'is_package'):
                try:
                    is_package = loader.is_package(name)
                except ImportError:
                    pass
                else:
                    if is_package:
                        spec.submodule_search_locations = []
        else:
            spec.submodule_search_locations = submodule_search_locations
        if spec.submodule_search_locations == []:
            if location:
                dirname = os.path.split(location)[0]
                spec.submodule_search_locations.append(dirname)

        return spec

    # Implementing spec_from_loader, ported from python3
    # to provide a py2/py3 API
    def spec_from_loader(name, loader, origin=None, is_package=None):
        """Return a module spec based on various loader methods."""
        if hasattr(loader, 'get_filename'):
            if is_package is None:
                return spec_from_file_location(name, loader=loader)
            search = [] if is_package else None
            return spec_from_file_location(name, loader=loader,
                                           submodule_search_locations=search)

        if is_package is None:
            if hasattr(loader, 'is_package'):
                try:
                    is_package = loader.is_package(name)
                except ImportError:
                    is_package = None  # aka, undefined
            else:
                # the default
                is_package = False
        return ModuleSpec(name, loader, origin=origin, is_package=is_package)


    class _NamespacePath:
        """Represents a namespace package's path.  It uses the module name
        to find its parent module, and from there it looks up the parent's
        __path__.  When this changes, the module's own path is recomputed,
        using path_finder.  For top-level modules, the parent module's path
        is sys.path."""

        def __init__(self, name, path, path_finder):
            self._name = name
            self._path = path
            self._last_parent_path = tuple(self._get_parent_path())
            self._path_finder = path_finder

        def _find_parent_path_names(self):
            """Returns a tuple of (parent-module-name, parent-path-attr-name)"""
            parent, dot, me = self._name.rpartition('.')
            if dot == '':
                # This is a top-level module. sys.path contains the parent path.
                return 'sys', 'path'
            # Not a top-level module. parent-module.__path__ contains the
            #  parent path.
            return parent, '__path__'

        def _get_parent_path(self):
            parent_module_name, path_attr_name = self._find_parent_path_names()
            return getattr(sys.modules[parent_module_name], path_attr_name)

        def _recalculate(self):
            # If the parent's path has changed, recalculate _path
            parent_path = tuple(self._get_parent_path())  # Make a copy
            if parent_path != self._last_parent_path:
                spec = self._path_finder(self._name, parent_path)
                # Note that no changes are made if a loader is returned, but we
                #  do remember the new parent path
                if spec is not None and spec.loader is None:
                    if spec.submodule_search_locations:
                        self._path = spec.submodule_search_locations
                self._last_parent_path = parent_path  # Save the copy
            return self._path

        def __iter__(self):
            return iter(self._recalculate())

        def __len__(self):
            return len(self._recalculate())

        def __repr__(self):
            return '_NamespacePath({!r})'.format(self._path)

        def __contains__(self, item):
            return item in self._recalculate()

        def append(self, item):
            self._path.append(item)

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

        @classmethod
        def _legacy_get_spec(cls, fullname, finder):
            # This would be a good place for a DeprecationWarning if
            # we ended up going that route.
            if hasattr(finder, 'find_loader'):
                loader, portions = finder.find_loader(fullname)
            else:
                loader = finder.find_module(fullname)
                portions = []
            if loader is not None:
                return spec_from_loader(fullname, loader)
            spec = ModuleSpec(fullname, None)
            spec.submodule_search_locations = portions
            return spec

        @classmethod
        def _get_spec(cls, fullname, path, target=None):
            """Find the loader or namespace_path for this module/package name."""
            # If this ends up being a namespace package, namespace_path is
            #  the list of paths that will become its __path__
            namespace_path = []
            for entry in path:
                if not isinstance(entry, (str, bytes)):
                    continue
                finder = cls._path_importer_cache(entry)
                if finder is not None:
                    if hasattr(finder, 'find_spec'):
                        spec = finder.find_spec(fullname, target)
                    else:
                        spec = cls._legacy_get_spec(fullname, finder)
                    if spec is None:
                        continue
                    if spec.loader is not None:
                        return spec
                    portions = spec.submodule_search_locations
                    if portions is None:
                        raise ImportError('spec missing loader')
                    # This is possibly part of a namespace package.
                    #  Remember these path entries (if any) for when we
                    #  create a namespace package, and continue iterating
                    #  on path.
                    namespace_path.extend(portions)
            else:
                spec = ModuleSpec(fullname, None)
                spec.submodule_search_locations = namespace_path
                return spec

        @classmethod
        def find_module(cls, fullname, path=None):
            """find the module on sys.path or 'path' based on sys.path_hooks and
            sys.path_importer_cache.
            This method is for python2 only
            """
            spec = cls.find_spec(fullname, path)
            if spec is None:
                return None
            return spec.loader

        @classmethod
        def find_spec(cls, fullname, path=None, target=None):
            """find the module on sys.path or 'path' based on sys.path_hooks and
            sys.path_importer_cache."""
            if path is None:
                path = sys.path
            spec = cls._get_spec(fullname, path, target)
            if spec is None:
                return None
            elif spec.loader is None:
                namespace_path = spec.submodule_search_locations
                if namespace_path:
                    # We found at least one namespace path.  Return a
                    #  spec which can create the namespace package.
                    spec.origin = 'namespace'
                    spec.submodule_search_locations = _NamespacePath(fullname, namespace_path, cls._get_spec)
                    return spec
                else:
                    return None
            else:
                return spec


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

        # @classmethod
        # def find_module(cls, fullname, path=None):  # from importlib.PathFinder
        #     """Try to find the module on sys.path or 'path'
        #     The search is based on sys.path_hooks and sys.path_importer_cache.
        #     """
        #     if path is None:
        #         path = sys.path
        #     loader = None
        #     for entry in path:
        #         if not isinstance(entry, (str, bytes)):
        #             continue
        #         finder = cls._path_importer_cache(entry)
        #         if finder is not None:
        #             loader = finder.find_module(fullname)
        #             if loader is not None:
        #                 break  # we stop at the first loader found
        #
        #     # if no loader was found, we need to start the namespace finding logic
        #     if loader is None:
        #         for entry in path:
        #             if not isinstance(entry, (str, bytes)):
        #                 continue
        #             base_path = os.path.join(entry, fullname.rpartition('.')[-1])
        #             if os.path.isdir(entry) and os.path.exists(base_path):  # this should now be considered a namespace
        #                 loader = NamespaceLoader2(fullname, base_path)
        #             if loader is not None:
        #                 break  # we stop at the first loader found
        #
        #     return loader


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

        def _get_spec(self, loader_class, fullname, path, smsl, target):
            loader = loader_class(fullname, path)
            return spec_from_file_location(fullname, path, loader=loader,
                                           submodule_search_locations=smsl)

        def find_spec(self, fullname, target=None):
            """Try to find a spec for the specified module.  Returns the
            matching spec, or None if not found."""
            is_namespace = False
            tail_module = fullname.rpartition('.')[2]

            base_path = os.path.join(self.path, tail_module)
            for suffix, loader_class in self._loaders:
                init_filename = '__init__' + suffix
                init_full_path = os.path.join(base_path, init_filename)
                full_path = base_path + suffix
                if os.path.isfile(init_full_path):
                    return self._get_spec(loader_class, fullname, full_path, [base_path], target)
                if os.path.isfile(full_path):  # maybe we need more checks here (importlib filefinder checks its cache...)
                    return self._get_spec(loader_class, fullname, full_path, None, target)
            else:
                # If a namespace package, return the path if we don't
                #  find a module in the next section.
                is_namespace = os.path.isdir(base_path)

            if is_namespace:
                _verbose_message('possible namespace for {}'.format(base_path))
                spec = ModuleSpec(fullname, None)
                spec.submodule_search_locations = [base_path]
                return spec
            return None

        # def find_spec(self, fullname, target=None):
        #     """ python3 latest API, to provide a py2/py3 extensible API """
        #     path = self.path
        #     tail_module = fullname.rpartition('.')[2]
        #
        #     base_path = os.path.join(path, tail_module)
        #     for suffix, loader_class in self._loaders:
        #         full_path = None  # adjusting path for package or file
        #         if os.path.isdir(base_path) and os.path.isfile(os.path.join(base_path, '__init__' + suffix)):
        #             # __init__.py path will be computed by the loader when needed
        #             loader = loader_class(fullname, base_path)
        #         elif os.path.isfile(base_path + suffix):
        #             loader = loader_class(fullname, base_path + suffix)
        #     loader = None
        #
        #     return spec_from_loader(fullname, loader)
        #
        # def find_module(self, fullname):
        #     """Try to find a loader for the specified module, or the namespace
        #     package portions. Returns loader.
        #     """
        #     # Call find_loader(). If it returns a string (indicating this
        #     # is a namespace package portion), generate a warning and
        #     # return None.
        #
        #     spec = self.find_spec(fullname)
        #     if spec is None:
        #         loader = None
        #         portions = []
        #     else:
        #         loader = spec.loader
        #         portions = spec.submodule_search_locations or []
        #
        #     if loader is None and len(portions):
        #         msg = 'Not importing directory {}: missing __init__'
        #         warnings.warn(msg.format(portions[0]), ImportWarning)
        #
        #     return loader

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

    # Making the activation explicit for now
    def activate():
        """Install the path-based import components."""
        supported_loaders = get_supported_file_loaders()
        path_hook = FileFinder2.path_hook(*supported_loaders)
        if path_hook not in sys.path_hooks:
            sys.path_hooks.append(path_hook)
        # Resetting sys.path_importer_cache values,
        # to support the case where we have an implicit package inside an already loaded package,
        # since we need to replace the default importer.
        sys.path_importer_cache.clear()

        if NamespaceMetaFinder2 not in sys.meta_path:
            # Setting up the meta_path to change package finding logic
            sys.meta_path.append(NamespaceMetaFinder2)

elif sys.version_info >= (3, 4):  # valid from which py3 version ?
    from importlib.machinery import (
        SOURCE_SUFFIXES, SourceFileLoader,
        BYTECODE_SUFFIXES, SourcelessFileLoader,
        EXTENSION_SUFFIXES, ExtensionFileLoader,
        PathFinder, FileFinder,
        ModuleSpec
    )

    from importlib.util import (
        spec_from_file_location,
        spec_from_loader
    )

    PathFinder2 = PathFinder
    FileFinder2 = FileFinder

    SourceFileLoader2 = SourceFileLoader
    SourcelessFileLoader2 = SourcelessFileLoader
    ExtensionFileLoader2 = ExtensionFileLoader

    # This is already defined in importlib._bootstrap_external
    # but is not exposed.
    def get_supported_file_loaders():
        """Returns a list of file-based module loaders.
        Each item is a tuple (loader, suffixes).
        """
        extensions = ExtensionFileLoader, EXTENSION_SUFFIXES
        source = SourceFileLoader, SOURCE_SUFFIXES
        bytecode = SourcelessFileLoader, BYTECODE_SUFFIXES
        return [extensions, source, bytecode]

    def activate():
        pass

else:
    raise ImportError("filefinder2 : Unsupported python version")
