from __future__ import absolute_import, print_function

# Simple module replicating importlib.machinery API of importlib in python3

from ._spec_utils import ModuleSpec
# BuiltinImporter Not Implemented
# FrozenImporter Not implemented
from ._fileloader2 import (
    SOURCE_SUFFIXES, BYTECODE_SUFFIXES, EXTENSION_SUFFIXES
)
# WindowsRegistryFinder
from ._filefinder2 import PathFinder2
from ._filefinder2 import FileFinder2
from ._fileloader2 import SourceFileLoader2
from ._fileloader2 import SourcelessFileLoader2
from ._fileloader2 import ExtensionFileLoader2


def all_suffixes():
    """Returns a list of all recognized module suffixes for this process"""
    return SOURCE_SUFFIXES + BYTECODE_SUFFIXES + EXTENSION_SUFFIXES


# For importlib API compatibility:
FileFinder = FileFinder2
PathFinder = PathFinder2
SourceFileLoader = SourceFileLoader2
SourcelessFileLoader = SourcelessFileLoader2
ExtensionFileLoader = ExtensionFileLoader2

