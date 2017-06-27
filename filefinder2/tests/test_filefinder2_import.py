from __future__ import absolute_import, print_function

import copy

"""
Testing rosmsg_import with import keyword.
CAREFUL : these tests should run with pytest --boxed in order to avoid polluting each other sys.modules
"""

import sys
import unittest

# CAREFUL : it seems this does have side effect in pytest modules and hooks setup.
from ._utils import print_importers
import filefinder2

# importlib
# https://pymotw.com/3/importlib/index.html
# https://pymotw.com/2/importlib/index.html


# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure
class TestImplicitNamespace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This should activate only for old python
        if (2, 7) <= sys.version_info < (3, 4):
            filefinder2.activate()
        # python3 implicit namespaces should work out of the box.

    def test_import_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        from .nspkg import subpkg as test_pkg

        self.assertTrue(test_pkg is not None)
        self.assertTrue(test_pkg.TestClassInSubPkg is not None)
        self.assertTrue(callable(test_pkg.TestClassInSubPkg))

    def test_import_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        from .nspkg.subpkg import submodule as test_mod

        self.assertTrue(test_mod is not None)
        self.assertTrue(test_mod.TestClassInSubModule is not None)
        self.assertTrue(callable(test_mod.TestClassInSubModule))

    def test_import_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__

        from .nspkg.subpkg import TestClassInSubPkg

        self.assertTrue(TestClassInSubPkg is not None)
        self.assertTrue(callable(TestClassInSubPkg))

    def test_import_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        from .nspkg.subpkg.submodule import TestClassInSubModule

        self.assertTrue(TestClassInSubModule is not None)
        self.assertTrue(callable(TestClassInSubModule))

    def test_import_relative_nonnspkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        with self.assertRaises(ImportError):
            from .bad_nspkg import bad_subpkg


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
