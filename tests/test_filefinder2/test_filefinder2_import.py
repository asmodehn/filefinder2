from __future__ import absolute_import, print_function

import copy

"""
Testing rosmsg_import with import keyword.
CAREFUL : these tests should run with pytest --boxed in order to avoid polluting each other sys.modules
"""

import os
import sys
import unittest
import pytest

# CAREFUL : it seems this does have side effect in pytest modules and hooks setup.
try:
    from ._utils import print_importers, xfail_py2_noff2, xfail_py2_noactive
except ValueError:  # "Attempted relative import in non-package" when running standalone
    from _utils import print_importers, xfail_py2_noff2, xfail_py2_noactive


# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure

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
        dest_pyc = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.pyc')  # CAREFUL where ?
        py_compile.compile(source_py, dest_pyc, doraise=True)

    def setUp(self):
        # filefinder2 will be imported and activated depending on command line options. see conftext.py
        assert hasattr(self, "importlib")

    def test_importlib_import_relative_pkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            from . import pkg as test_pkg

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_pkg)
            else:
                pass

    def test_importlib_import_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.submodule'))
        else:
            from .pkg import submodule as test_mod

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    def test_importlib_import_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            from .pkg import bytecode as test_mod

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInBytecode is not None)
            self.assertTrue(callable(test_mod.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(test_mod)
            else:
                pass

    def test_importlib_import_class_from_relative_pkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            from . import pkg
            test_class_in_subpkg = pkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(pkg)
            else:
                pass

    def test_importlib_import_class_from_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.submodule'))
        else:
            from .pkg import submodule
            test_class_in_submodule = submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(submodule)
            else:
                pass

    def test_importlib_import_class_from_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # need globals to handle relative imports
        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            from .pkg import bytecode
            test_class_in_bytecode = bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(bytecode)
            else:
                pass

    def test_importlib_import_relative_badpkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.badpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.badpkg'))
        else:
            with self.assertRaises(ImportError):
                from . import badpkg

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            from .nspkg import subpkg as test_pkg

            self.assertTrue(test_pkg is not None)
            self.assertTrue(test_pkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(test_pkg.TestClassInSubPkg))

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            from .nspkg.subpkg import submodule as test_mod

            self.assertTrue(test_mod is not None)
            self.assertTrue(test_mod.TestClassInSubModule is not None)
            self.assertTrue(callable(test_mod.TestClassInSubModule))

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_relative_ns_subpkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.bytecode'))
        else:
            from .nspkg.subpkg import bytecode as test_bc

            self.assertTrue(test_bc is not None)
            self.assertTrue(test_bc.TestClassInBytecode is not None)
            self.assertTrue(callable(test_bc.TestClassInBytecode))

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            from .nspkg.subpkg import TestClassInSubPkg

            self.assertTrue(TestClassInSubPkg is not None)
            self.assertTrue(callable(TestClassInSubPkg))

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg.submodule'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.submodule'))
        else:
            from .nspkg.subpkg.submodule import TestClassInSubModule

            self.assertTrue(TestClassInSubModule is not None)
            self.assertTrue(callable(TestClassInSubModule))

    @xfail_py2_noff2
    @xfail_py2_noactive
    def test_import_class_from_relative_ns_subpkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            from .nspkg.subpkg.bytecode import TestClassInBytecode

            self.assertTrue(TestClassInBytecode is not None)
            self.assertTrue(callable(TestClassInBytecode))

    def test_import_relative_nonnspkg_raises(self):
        """Verify that bad package is not importable relatively"""
        print_importers()
        assert __package__

        # import checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.bad_nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.bad_nspkg'))
        else:
            with self.assertRaises(ImportError):
                from .bad_nspkg import bad_subpkg


# TODO  : test deriving an importer from filefinder2 to test the extension usage (like done in rosimporter or palimport)

if __name__ == '__main__':
    import pytest
    # testing current python capabilities
    pytest.main(['-v', '-s', '--noff2', '-x', __file__, '--forked'])
    # testing importing ff2 does not disturb anything
    pytest.main(['-v', '-s', '--noactive', '-x', __file__, '--forked'])
    # testing ff2 features
    pytest.main(['-v', '-s', '-x', __file__, '--forked'])
