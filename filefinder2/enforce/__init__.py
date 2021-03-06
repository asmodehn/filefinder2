"""

Package to import directly, to use the backward compatible classes, even in python3.
It can be helpful for debugging import-time issues, but is definitely:

!!! NOT FOR EVERYDAY USE !!!

"""

import sys
import contextlib

from .machinery import (
    PathFinder,
    FileFinder,
    # extra API (not exposed in importlib) useful when defining extensions of basic python import
    ff_path_hook,
    get_supported_file_loaders,
)

# Public API #########################################################


# Making the activation explicit for now
def activate():
    """Install the path-based import components."""

    global PathFinder, FileFinder, ff_path_hook

    path_hook_index = len(sys.path_hooks)
    sys.path_hooks.append(ff_path_hook)
    # Resetting sys.path_importer_cache values,
    # to support the case where we have an implicit package inside an already loaded package,
    # since we need to replace the default importer.
    sys.path_importer_cache.clear()

    # Setting up the meta_path to change package finding logic
    pathfinder_index = len(sys.meta_path)
    sys.meta_path.append(PathFinder)

    return path_hook_index, pathfinder_index


def deactivate(path_hook_index, pathfinder_index, force=False):
    # CAREFUL : Even though we remove the path from sys.path,
    # initialized finders will remain in sys.path_importer_cache

    # removing metahook
    sys.meta_path.pop(pathfinder_index)
    sys.path_hooks.pop(path_hook_index)

    # Resetting sys.path_importer_cache to get rid of previous importers
    sys.path_importer_cache.clear()


@contextlib.contextmanager
def enable_pep420():
    """
    Enabling support of pep420, now available on python2
    :param force: if set, filefinder2 code will be enabled for python3 as well.
    CAREFUL : this is only intended for import-time debugging purposes from python code.
    :return:
    """
    path_hook_index, pathfinder_index = activate()
    yield path_hook_index, pathfinder_index
    deactivate(path_hook_index, pathfinder_index)
