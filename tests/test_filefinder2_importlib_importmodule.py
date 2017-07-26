from __future__ import absolute_import, print_function
"""
Testing import statement with filefinder2
"""

import os
import sys
import unittest
import pytest  # we need to use pytest marker to get __package__ to get the proper value, making relative import works


# CAREFUL : it seems this does have side effect in pytest modules and hooks setup.
from ._utils import print_importers


# To test that we actually have the same API as importlib
import filefinder2, filefinder2.util
filefinder2.activate()
importlib = filefinder2
importlib.util = filefinder2.util

# importlib
# https://pymotw.com/3/importlib/index.html
# https://pymotw.com/2/importlib/index.html

#
# Note : we cannot assume anything about import implementation (different python version, different version of pytest)
# => we need to test them all...
#


# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure
class WrapperToHideUnittestCase:
    # TODO : depending on the python version we aim to support, we might be able to drop some tests here...
    class TestImplicitNamespace(unittest.TestCase):
        """
        Testing PEP 420
        """

        # Using import_module
        # TODO pkg
        def test_importlib_importmodule_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import_module checks sys.modules by itself
            test_pkg = importlib.import_module('.nspkg.subpkg', package=__package__)

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_pkg)
            else:
                pass

        def test_importlib_importmodule_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import_module checks sys.modules by itself
            test_mod = importlib.import_module('.nspkg.subpkg.submodule', package=__package__)

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_importmodule_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # import_module checks sys.modules by itself
            test_mod = importlib.import_module('.nspkg.subpkg.bytecode', package=__package__)

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_importmodule_class_from_relative_ns_subpkg(self):
            """Verify that test class is importable relatively"""
            print_importers()
            assert __package__
            # import_module checks sys.modules by itself
            nspkg_subpkg = importlib.import_module('.nspkg.subpkg', package=__package__)
            TestClassInSubPkg = nspkg_subpkg.TestClassInSubPkg

            self.assertTrue(TestClassInSubPkg is not None)
            self.assertTrue(callable(TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg_subpkg)
            else:
                pass

        def test_importlib_importmodule_class_from_relative_ns_subpkg_submodule(self):
            """Verify that test class is importable relatively"""
            print_importers()
            assert __package__
            # import_module checks sys.modules by itself
            nspkg_subpkg_submodule = importlib.import_module('.nspkg.subpkg.submodule', package=__package__)
            TestClassInSubModule = nspkg_subpkg_submodule.TestClassInSubModule

            self.assertTrue(TestClassInSubModule is not None)
            self.assertTrue(callable(TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg_subpkg_submodule)
            else:
                pass

        def test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode(self):
            """Verify that test class is importable relatively"""
            print_importers()
            assert __package__
            # import_module checks sys.modules by itself
            nspkg_subpkg_bytecode = importlib.import_module('.nspkg.subpkg.bytecode', package=__package__)
            TestClassInBytecode = nspkg_subpkg_bytecode.TestClassInBytecode

            self.assertTrue(TestClassInBytecode is not None)
            self.assertTrue(callable(TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg_subpkg_bytecode)
            else:
                pass

        def test_importlib_importmodule_relative_nonnspkg_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            with self.assertRaises(ImportError):
                importlib.import_module('.bad_nspkg', package=__package__)


class TestImplicitNamespaceRaw(WrapperToHideUnittestCase.TestImplicitNamespace):
    """
    Testing PEP 420
    """

    @classmethod
    def setUpClass(cls):
        # we compile the bytecode with the testing python interpreter
        import py_compile
        source_py = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode_source.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)
        source_py = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode_source.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)


class TestImplicitNamespaceFF2(WrapperToHideUnittestCase.TestImplicitNamespace):
    """
    Testing PEP 420
    """

    @classmethod
    def setUpClass(cls):
        # we compile the bytecode with the testing python interpreter
        import py_compile
        source_py = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode_source.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)
        source_py = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode_source.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)

        import filefinder2 as importlib
        importlib.activate()
        # Note : filefinder2 will also be used with python3, but it should internally use importlib.


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
