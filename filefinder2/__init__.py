from __future__ import absolute_import, print_function

"""A Python2 and Python3 implementation of import."""
__all__ = ['__import__', 'import_module', 'invalidate_caches', 'reload']

# Note : here we do not need to bootstrap like python's importlib

import imp
import sys
import six

import types
import warnings

from ._utils import _ImportError

from ._filefinder2 import activate, deactivate
from ._filefinder2 import get_filefinder_index_in_path_hooks, get_pathfinder_index_in_meta_hooks

# extra API (not exposed in importlib) useful when defining extensions of basic python import
from ._fileloader2 import get_supported_file_loaders

# Public API #########################################################


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
