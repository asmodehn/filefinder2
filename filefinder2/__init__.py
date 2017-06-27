from __future__ import absolute_import, print_function

import sys

from ._filefinder2 import _install_hook

# Making the activation explicit for now
def activate():
    _install_hook()
