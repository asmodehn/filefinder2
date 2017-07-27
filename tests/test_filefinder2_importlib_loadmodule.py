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

        def test_importlib_loadmodule_relative_pkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

            self.assertTrue(pkg is not None)
            self.assertTrue(pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(pkg.TestClassInSubPkg))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_relative_pkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

            # here we should get the module that has already be loaded while executing subpkg
            submodule = sys.modules.get(__package__ + '.pkg.submodule')

            self.assertTrue(submodule is not None)
            self.assertTrue(submodule.TestClassInSubModule is not None)
            self.assertTrue(callable(submodule.TestClassInSubModule))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_relative_pkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            bytecode_loader = importlib.find_loader(__package__ + '.pkg.bytecode', pkg.__path__)
            bytecode = bytecode_loader.load_module(__package__ + '.pkg.bytecode')
            # safely adding to sysmodules to be able to perform relative imports in there
            # sys.modules.setdefault(subpkg.__name__, subpkg)

            self.assertTrue(bytecode is not None)
            self.assertTrue(bytecode.TestClassInBytecode is not None)
            self.assertTrue(callable(bytecode.TestClassInBytecode))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_class_from_relative_pkg(self):
            """Verify that message class is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

            test_class_in_subpkg = pkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_class_from_relative_pkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(pkg.__name__, nspkg)

            # here we should get the module that has already be loaded while executing subpkg
            submodule = sys.modules.get(__package__ + '.pkg.submodule')

            test_class_in_submodule = submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_class_from_relative_pkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            bytecode_loader = importlib.find_loader(__package__ + '.pkg.bytecode', pkg.__path__)
            bytecode = bytecode_loader.load_module(__package__ + '.pkg.bytecode')
            # safely adding to sysmodules to be able to perform relative imports in there
            # sys.modules.setdefault(subpkg.__name__, subpkg)

            test_class_in_bytecode = bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # Note : apparently reload is broken with find_loader (at least on python 3.5)
            # _find_spec in reload() apparently returns None...
            #
            # => not testing reload in that case (this API is obsolete anyway)

        def test_importlib_loadmodule_relative_badpkg_returns_none(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            assert importlib.find_loader(__package__ + '.bad_pkg', [os.path.dirname(__file__)]) is None

        def test_importlib_loadmodule_relative_ns_subpkg_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            with self.assertRaises(ImportError):  # namespace packages do not have loaders
                # Note if this passes, it might be that ANOTHER way of doing import loaded the module,
                # and you got a bwcompat loader in sys.modules, which gets reused
                importlib.find_loader(__package__ + '.nspkg', [os.path.dirname(__file__)])


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
