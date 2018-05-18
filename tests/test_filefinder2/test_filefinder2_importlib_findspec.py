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

# Because python 3.4 has issues with util.module_from_spec
#: expect failure if we are in python2 and did NOT import filefinder2
xfail_py34_noff2 = pytest.mark.xfail(  # we need a string there to access the config at runtime
    "(pytest.config.getoption('--noff2')) and sys.version_info < (3, 5)",
    reason="python 3.4 has issues with util.module_from_spec without importing filefinder2",
    strict=True
)

#: expect failure if we imported filefinder2 but did NOT activate it
xfail_py34_noactive = pytest.mark.xfail(  # we need a string there to access the config at runtime
    "(pytest.config.getoption('--noactive')) and sys.version_info < (3, 5)",
    reason="python 3.4 has issues with util.module_from_spec without activating filefinder2",
    strict=True
)

#
# Note : we cannot assume anything about import implementation (different python version, different version of pytest)
# => we need to test them all...
#

# TODO : the tests here can still be improved,along with filefinder2, to provide python3 importlib full API on python2
# TODO : when filefinder2 is imported, even if we do not support namespace packages.

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
        dest_pyc = os.path.join(os.path.dirname(__file__), 'nspkg', 'subpkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)
        source_py = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.py')
        dest_pyc = os.path.join(os.path.dirname(__file__), 'pkg', 'bytecode.pyc')  # CAREFUL where
        py_compile.compile(source_py, dest_pyc, doraise=True)

    def setUp(self):
        # filefinder2 will be imported and activated depending on command line options. see conftext.py
        assert hasattr(self, "importlib")

    # using find_spec and module_from_spec
    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_pkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

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

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

            # pkg execution already imported pkg.submodule
            submodule = pkg.submodule

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

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

            # pkg execution DID NOT import pkg.bytecode (not imported in __init__)
            # bytecode = pkg.bytecode

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            bytecode_spec = self.importlib.util.find_spec('.pkg.bytecode', __package__)
            bytecode = self.importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we don't do this for a namespace package
                bytecode_spec.loader.exec_module(bytecode)

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

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_pkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__
        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

            test_class_in_subpkg = pkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(pkg)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_pkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

            # pkg execution already imported pkg.submodule
            submodule = pkg.submodule

            test_class_in_submodule = submodule.TestClassInSubModule

            self.assertTrue(test_class_in_submodule is not None)
            self.assertTrue(callable(test_class_in_submodule))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(submodule)
            else:
                pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_pkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg'))
        else:
            pkg_spec = self.importlib.util.find_spec('.pkg', __package__)
            pkg = self.importlib.util.module_from_spec(pkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(pkg.__name__, pkg)
            if pkg_spec.loader:
                # we don't do this for a namespace package
                pkg_spec.loader.exec_module(pkg)

            # pkg execution DID NOT import pkg.bytecode (not imported in __init__)
            # bytecode = pkg.bytecode

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.pkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.pkg.bytecode'))
        else:
            bytecode_spec = self.importlib.util.find_spec('.pkg.bytecode', __package__)
            bytecode = self.importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we don't do this for a namespace package
                bytecode_spec.loader.exec_module(bytecode)

            test_class_in_bytecode = bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(self.importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                self.importlib.reload(bytecode)
            else:
                pass

    @xfail_py2_noff2
    def test_importlib_findspec_relative_badpkg_isnone(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # __import__ checks sys.modules by itself
        # but the test is not reflecting anything if we use the already loaded module.
        if sys.modules.get(__package__ + '.badpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.badpkg'))
        else:
            badpkg_spec = self.importlib.util.find_spec('.badpkg', __package__)
            assert badpkg_spec is None

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        self.assertTrue(subpkg is not None)
        self.assertTrue(subpkg.TestClassInSubPkg is not None)
        self.assertTrue(callable(subpkg.TestClassInSubPkg))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(subpkg)
        else:
            pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        # here we should get the module that has already be loaded while executing subpkg
        submodule = sys.modules.get(__package__ + '.nspkg.subpkg.submodule')

        self.assertTrue(submodule is not None)
        self.assertTrue(submodule.TestClassInSubModule is not None)
        self.assertTrue(callable(submodule.TestClassInSubModule))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(submodule)
        else:
            pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_relative_ns_subpkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.bytecode'))
        else:
            # bytecode is not imported hwen executing the __init__ module, so we need to import it separately here
            bytecode_spec = self.importlib.util.find_spec('.nspkg.subpkg.bytecode', __package__)
            bytecode = self.importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we do this for a normal package
                bytecode_spec.loader.exec_module(bytecode)

        self.assertTrue(bytecode is not None)
        self.assertTrue(bytecode.TestClassInBytecode is not None)
        self.assertTrue(callable(bytecode.TestClassInBytecode))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(bytecode)
        else:
            pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        test_class_in_subpkg = subpkg.TestClassInSubPkg

        self.assertTrue(test_class_in_subpkg is not None)
        self.assertTrue(callable(test_class_in_subpkg))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(nspkg)
        else:
            pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        # here we should get the module that has already be loaded while executing subpkg
        submodule = sys.modules.get(__package__ + '.nspkg.subpkg.submodule')

        test_class_in_submodule = submodule.TestClassInSubModule

        self.assertTrue(test_class_in_submodule is not None)
        self.assertTrue(callable(test_class_in_submodule))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(nspkg)
        else:
            pass

    @xfail_py2_noff2
    @xfail_py2_noactive
    @xfail_py34_noff2
    @xfail_py34_noactive
    def test_importlib_findspec_class_from_relative_ns_subpkg_bytecode(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg'))
        else:
            nspkg_spec = self.importlib.util.find_spec('.nspkg', __package__)
            nspkg = self.importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg'))
        else:
            subpkg_spec = self.importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = self.importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

        # we need to check sys.modules before doing anything
        if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
            self.fail("module {0} previously loaded. You might need to fix your tests to run with --forked.".format(__package__ + '.nspkg.subpkg.bytecode'))
        else:
            bytecode_spec = self.importlib.util.find_spec('.nspkg.subpkg.bytecode', __package__)
            bytecode = self.importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we do this for a normal package
                bytecode_spec.loader.exec_module(bytecode)

        test_class_in_bytecode = bytecode.TestClassInBytecode

        self.assertTrue(test_class_in_bytecode is not None)
        self.assertTrue(callable(test_class_in_bytecode))

        # TODO : implement some differences and check we get them...
        if hasattr(self.importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            self.importlib.reload(nspkg)
        else:
            pass

    @xfail_py2_noff2
    def test_importlib_findspec_relative_nonnspkg_returns_none(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        assert self.importlib.util.find_spec('.bad_nspkg', __package__) is None


if __name__ == '__main__':
    import pytest
    # testing current python capabilities
    pytest.main(['-v', '-s', '--noff2', '-x', __file__, '--forked'])
    # testing importing ff2 provides importlib API but does not disturb anything
    pytest.main(['-v', '-s', '--noactive', '-x', __file__, '--forked'])
    # testing ff2 features
    pytest.main(['-v', '-s', '-x', __file__, '--forked'])
