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

    # Using import_module
    def test_importlib_importmodule_relative_pkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg = self.importlib.import_module('.pkg', package=__package__)
            test_pkg = pkg

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_pkg)
            else:
                pass

    def test_importlib_importmodule_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.submodule'))
        else:
            submodule = self.importlib.import_module('.pkg.submodule', package=__package__)
            test_mod = submodule

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    def test_importlib_importmodule_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            bytecode = self.importlib.import_module('.pkg.bytecode', package=__package__)
            test_mod = bytecode

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    def test_importlib_importmodule_class_from_relative_pkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg = self.importlib.import_module('.pkg', package=__package__)
            test_class_in_subpkg = pkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(pkg)
            else:
                pass

    def test_importlib_importmodule_class_from_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.submodule'))
        else:
            submodule = self.importlib.import_module('.pkg.submodule', package=__package__)
            test_class_in_submodule = submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(submodule)
            else:
                pass

    def test_importlib_importmodule_class_from_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            bytecode = self.importlib.import_module('.pkg.bytecode', package=__package__)
            test_class_in_bytecode = bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(bytecode)
            else:
                pass

    def test_importlib_importmodule_relative_badpkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.badpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.badpkg'))
        else:
            with self.assertRaises(ImportError):
                self.importlib.import_module('.badpkg', package=__package__)

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            test_pkg = self.importlib.import_module('.nspkg.subpkg', package=__package__)

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_pkg)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.submodule'))
        else:
            test_mod = self.importlib.import_module('.nspkg.subpkg.submodule', package=__package__)

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_relative_ns_subpkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.bytecode'))
        else:
            test_mod = self.importlib.import_module('.nspkg.subpkg.bytecode', package=__package__)

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_class_from_relative_ns_subpkg(self):
        """Verify that test class is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            nspkg_subpkg = self.importlib.import_module('.nspkg.subpkg', package=__package__)
            test_class_in_subpkg = nspkg_subpkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(nspkg_subpkg)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_class_from_relative_ns_subpkg_submodule(self):
        """Verify that test class is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.submodule'))
        else:
            nspkg_subpkg_submodule = self.importlib.import_module('.nspkg.subpkg.submodule', package=__package__)
            test_class_in_submodule = nspkg_subpkg_submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(nspkg_subpkg_submodule)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode(self):
        """Verify that test class is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.bytecode'))
        else:
            nspkg_subpkg_bytecode = self.importlib.import_module('.nspkg.subpkg.bytecode', package=__package__)
            test_class_in_bytecode = nspkg_subpkg_bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(nspkg_subpkg_bytecode)
            else:
                pass

    def test_importlib_importmodule_relative_nonnspkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import_module checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.bad_nspkg.bad_subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.bad_nspkg.bad_subpkg'))
        else:
            with self.assertRaises(ImportError):
                self.importlib.import_module('.bad_nspkg.bad_subpkg', package=__package__)


if __name__ == '__main__':
    import pytest
    # testing current python capabilities
    pytest.main(['-v', '-s', '--noff2', '-x', __file__, '--forked'])
    # testing importing ff2 does not disturb anything
    pytest.main(['-v', '-s', '--noactive', '-x', __file__, '--forked'])
    # testing ff2 features
    pytest.main(['-v', '-s', '-x', __file__, '--forked'])
