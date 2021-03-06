from __future__ import absolute_import, print_function

import sys

# Simple module replicating importlib.machinery API of importlib in python3
# This is just the "except" clauses from the non enforced version

from .._spec_utils import ModuleSpec

# BuiltinImporter Not Implemented
# FrozenImporter Not implemented
# WindowsRegistryFinder

from .._fileloader2 import (
    SOURCE_SUFFIXES_2, BYTECODE_SUFFIXES_2, EXTENSION_SUFFIXES_2
    # Note some of these will be different than a full fledged python import implementation.
)
SOURCE_SUFFIXES = SOURCE_SUFFIXES_2
BYTECODE_SUFFIXES = BYTECODE_SUFFIXES_2
EXTENSION_SUFFIXES = EXTENSION_SUFFIXES_2


# Should manage multiple python version by itself
def get_supported_file_loaders():
    from .._fileloader2 import get_supported_file_loaders_2
    return get_supported_file_loaders_2(force=True)


def all_suffixes():
    """Returns a list of all recognized module suffixes for this process"""
    return SOURCE_SUFFIXES + BYTECODE_SUFFIXES + EXTENSION_SUFFIXES


from .._fileloader2 import SourceFileLoader2
from .._fileloader2 import ImpFileLoader2
# to be compatible with py3 importlib
SourceFileLoader = SourceFileLoader2
SourcelessFileLoader = ImpFileLoader2
ExtensionFileLoader = ImpFileLoader2


from .._filefinder2 import PathFinder2
PathFinder = PathFinder2


from .._filefinder2 import FileFinder2
FileFinder = FileFinder2
ff_path_hook = FileFinder2.path_hook(*get_supported_file_loaders())

#
# def get_pathfinder_index_in_meta_hooks():
#     return sys.meta_path.index(PathFinder)
#
#
# def get_filefinder_index_in_path_hooks():
#     # Note the python version distinction is made at import time on ff_path_hook
#     return sys.path_hooks.index(ff_path_hook)
#




