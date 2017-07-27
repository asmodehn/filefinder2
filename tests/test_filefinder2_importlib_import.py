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

        # Using __import__
        def test_importlib_import_relative_pkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            # __import__ checks sys.modules by itself
            pkg = importlib.__import__('pkg', globals=globals(), level=1)
            test_pkg = pkg

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_pkg)
            else:
                pass

        def test_importlib_import_relative_pkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            # __import__ checks sys.modules by itself
            pkg = importlib.__import__('pkg.submodule', globals=globals(), level=1)
            test_mod = pkg.submodule

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_import_relative_pkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            # __import__ checks sys.modules by itself
            pkg = importlib.__import__('pkg.bytecode', globals=globals(), level=1)
            test_mod = pkg.bytecode

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_import_class_from_relative_pkg(self):
            """Verify that message class is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            # __import__ checks sys.modules by itself
            pkg = importlib.__import__('pkg', globals=globals(), level=1)
            test_class_in_subpkg = pkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(pkg)
            else:
                pass

        def test_importlib_import_class_from_relative_pkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            # __import__ checks sys.modules by itself
            pkg = importlib.__import__('pkg.submodule', globals=globals(), level=1)
            test_class_in_submodule = pkg.submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(pkg)
            else:
                pass

        def test_importlib_import_class_from_relative_pkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            # need globals to handle relative imports
            pkg = importlib.__import__('pkg.bytecode', globals=globals(), level=1)
            test_class_in_bytecode = pkg.bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(pkg)
            else:
                pass

        def test_importlib_import_relative_badpkg_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            with self.assertRaises(ImportError):
                importlib.__import__('badpkg', globals=globals(),
                                     level=1)  # need globals to handle relative imports

        def test_importlib_import_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_pkg = nspkg.subpkg

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_pkg)
            else:
                pass

        def test_importlib_import_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg.submodule', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_mod = nspkg.subpkg.submodule

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_import_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg.bytecode', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_mod = nspkg.subpkg.bytecode

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(test_mod)
            else:
                pass

        def test_importlib_import_class_from_relative_ns_subpkg(self):
            """Verify that message class is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_class_in_subpkg = nspkg.subpkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_import_class_from_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg.submodule', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_class_in_submodule = nspkg.subpkg.submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_import_class_from_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg = importlib.__import__('nspkg.subpkg.bytecode', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            test_class_in_bytecode = nspkg.subpkg.bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_import_relative_nonnspkg_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            with self.assertRaises(ImportError):
                importlib.__import__('bad_nspkg.bad_subpkg', globals=globals(), level=1)  # need globals to handle relative imports


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
