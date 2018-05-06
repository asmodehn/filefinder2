from __future__ import absolute_import, print_function

"""A Python2 and Python3 implementation of import."""
__all__ = ['__import__', 'import_module', 'invalidate_caches', 'reload']

# Note : here we do not need to bootstrap like python's importlib

import imp
import sys
import six

import types
import warnings
import contextlib

from ._utils import _ImportError

from .machinery import (
    PathFinder,
    FileFinder,
    # extra API (not exposed in importlib) useful when defining extensions of basic python import
    ff_path_hook,
    get_supported_file_loaders,
    get_filefinder_index_in_path_hooks,
    get_pathfinder_index_in_meta_hooks,
)


# Public API #########################################################


# Making the activation explicit for now
def activate(force=False):
    """Install the path-based import components."""

    global PathFinder, FileFinder, ff_path_hook

    if (2, 7) <= sys.version_info < (3, 4):
        if ff_path_hook not in sys.path_hooks:
            sys.path_hooks.append(ff_path_hook)

        if PathFinder not in sys.meta_path:
            # Setting up the meta_path to change package finding logic
            sys.meta_path.append(PathFinder)

    elif sys.version_info >= (3, 4):  # valid from which py3 version ?
        pass

    else:
        raise ImportError("filefinder2 : Unsupported python version")

    # Resetting sys.path_importer_cache values,
    # to support the (usual) case where we have an implicit package or a module inside an already loaded package,
    # since we need to replace the default importer.
    sys.path_importer_cache.clear()
    # Note : without this, newly added filefinder.find_spec will NOT be called,
    # Since filefinder was probably already cached for most locations.


def deactivate(force=False):
    if force or (2, 7) <= sys.version_info < (3, 4):
        # CAREFUL : Even though we remove the path from sys.path,
        # initialized finders will remain in sys.path_importer_cache

        # removing metahook
        sys.meta_path.pop(get_pathfinder_index_in_meta_hooks())
        sys.path_hooks.pop(get_filefinder_index_in_path_hooks())

        # Resetting sys.path_importer_cache to get rid of previous importers
        sys.path_importer_cache.clear()

    elif sys.version_info >= (3, 4):  # valid from which py3 version ?
        pass

    else:
        raise ImportError("filefinder2 : Unsupported python version")


@contextlib.contextmanager
def enable_pep420():
    """
    Enabling support of pep420, now available on python2
    :param force: if set, filefinder2 code will be enabled for python3 as well.
    CAREFUL : this is only intended for import-time debugging purposes from python code.
    :return:
    """
    activate()
    yield
    deactivate()

try:
    from importlib import invalidate_caches
except ImportError:
    def invalidate_caches():
        """Call the invalidate_caches() method on all meta path finders stored in
        sys.meta_path (where implemented)."""
        for finder in sys.meta_path:
            if hasattr(finder, 'invalidate_caches'):
                finder.invalidate_caches()

try:
    from importlib import find_loader
except ImportError:
    from ._spec_utils import _find_spec

    def find_loader(name, path=None):
        """Return the loader for the specified module.

        This is a backward-compatible wrapper around find_spec().

        This function is deprecated in favor of importlib.util.find_spec().

        """
        warnings.warn('Use importlib.util.find_spec() instead.',
                      DeprecationWarning, stacklevel=2)
        try:
            loader = sys.modules[name].__loader__
            if loader is None:
                raise ValueError('{}.__loader__ is None'.format(name))
            else:
                return loader
        except KeyError:
            pass
        except AttributeError:
            six.raise_from(ValueError('{}.__loader__ is not set'.format(name)), None)

        spec = _find_spec(name, path)
        # We won't worry about malformed specs (missing attributes).
        if spec is None:
            return None
        if spec.loader is None:
            if spec.submodule_search_locations is None:
                raise _ImportError('spec for {} missing loader'.format(name),
                                  name=name)
            raise _ImportError('namespace packages do not have loaders',
                              name=name)
        return spec.loader


# This should be in all python >2.7
from importlib import import_module

try:
    from importlib import __import__
except ImportError:
    # using the builtin method
    __import__ = __import__


try:
    from importlib import reload
except ImportError:

    from ._module_utils import module_from_spec
    from imp import reload

    _RELOADING = {}

    def reload(module):
        """Reload the module and return it.

        The module must have been successfully imported before.

        """
        if not module or not isinstance(module, types.ModuleType):
            raise TypeError("reload() argument must be a module")
        try:
            name = module.__spec__.name
        except AttributeError:
            name = module.__name__

        if sys.modules.get(name) is not module:
            msg = "module {} not in sys.modules"
            raise _ImportError(msg.format(name), name=name)
        if name in _RELOADING:
            return _RELOADING[name]
        _RELOADING[name] = module
        try:
            reload(module)

            # The module may have replaced itself in sys.modules!
            return sys.modules[name]
        finally:
            try:
                del _RELOADING[name]
            except KeyError:
                pass
