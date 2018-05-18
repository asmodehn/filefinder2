from __future__ import absolute_import, print_function
"""
Testing import statement with filefinder2
"""

import os
import sys
import unittest
import pytest  # we need to use pytest marker to get __package__ to get the proper value, making relative import works


# CAREFUL : it seems this does have side effect in pytest modules and hooks setup.
try:
    from ._utils import print_importers, xfail_py2_noff2, xfail_py2_noactive
except ValueError:  # "Attempted relative import in non-package" when running standalone
    from _utils import print_importers, xfail_py2_noff2, xfail_py2_noactive

#
# Note : we cannot assume anything about import implementation (different python version, different version of pytest)
# => we need to test them all...
#

# Note : This test is currently somehow approximate, since find_loader is already deprecated.

# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure

# TODO : depending on the python version we aim to support, we might be able to drop some tests here...
@pytest.mark.usefixtures("importlib")
class TestImplicitNamespace(unittest.TestCase):
    """
    Testing PEP 420
    """

    @classmethod
    def setUpClass(cls):
        # we compile the bytecode with the testing python interpreter
        import py_compile
        source_py = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)
        source_py = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)

    def setUp(self):
        # filefinder2 will be imported and activated depending on command line options. see conftext.py
        assert hasattr(self, "importlib")

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_relative_pkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
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

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
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

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            bytecode_loader = self.importlib.find_loader(__package__ + '.pkg.bytecode', pkg.__path__)
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

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_class_from_relative_pkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__

        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
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

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_class_from_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
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

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_class_from_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            pkg_loader = self.importlib.find_loader(__package__ + '.pkg', [os.path.dirname(__file__)])
            pkg = pkg_loader.load_module(__package__ + '.pkg')
            # safely adding to sysmodules to be able to perform relative imports in there
            #sys.modules.setdefault(nspkg.__name__, nspkg)

        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            # load_module returns existing modules from sys.modules by specification
            # see https://docs.python.org/3.3/library/importlib.html#importlib.abc.Loader)
            bytecode_loader = self.importlib.find_loader(__package__ + '.pkg.bytecode', pkg.__path__)
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

    @xfail_py2_noff2
    def test_importlib_loadmodule_relative_badpkg_returns_none(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        assert self.importlib.find_loader(__package__ + '.bad_pkg', [os.path.dirname(__file__)]) is None

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_loadmodule_relative_ns_subpkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            with self.assertRaises(ImportError):  # namespace packages do not have loaders
                # Note if this passes, it might be that ANOTHER way of doing import loaded the module,
                # and you got a bwcompat loader in sys.modules, which gets reused
                self.importlib.find_loader(__package__ + '.nspkg', [os.path.dirname(__file__)])


if __name__ == '__main__':
    import pytest
    # testing current python capabilities
    pytest.main(['-v', '-s', '--noff2', '-x', __file__, '--forked'])
    # testing importing ff2 does not disturb anything
    pytest.main(['-v', '-s', '--noactive', '-x', __file__, '--forked'])
    # testing ff2 features
    pytest.main(['-v', '-s', '-x', __file__, '--forked'])
