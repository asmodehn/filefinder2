from __future__ import absolute_import, print_function

# Simple module replicating importlib.machinery API of importlib in python3

from ._spec_utils import ModuleSpec
# BuiltinImporter Not Implemented
# FrozenImporter Not implemented
from ._fileloader2 import (
    SOURCE_SUFFIXES, BYTECODE_SUFFIXES, EXTENSION_SUFFIXES
    # Note some of these will be different than a full fledged python import implementation.
)
# WindowsRegistryFinder
from ._filefinder2 import PathFinder
from ._filefinder2 import FileFinder

from ._fileloader2 import SourceFileLoader
from ._fileloader2 import SourcelessFileLoader
from ._fileloader2 import ExtensionFileLoader


def all_suffixes():
    """Returns a list of all recognized module suffixes for this process"""
    return SOURCE_SUFFIXES + BYTECODE_SUFFIXES + EXTENSION_SUFFIXES


