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
            pkg = importlib.__import__('pkg', globals=globals(), level=1)  # need globals to handle relative imports
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
            pkg = importlib.__import__('pkg.submodule', globals=globals(),
                                         level=1)  # need globals to handle relative imports
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
            pkg = importlib.__import__('pkg.bytecode', globals=globals(),
                                         level=1)  # need globals to handle relative imports
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
            pkg = importlib.__import__('pkg', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            TestClassInSubPkg = pkg.TestClassInSubPkg

            self.assertTrue(TestClassInSubPkg is not None)
            self.assertTrue(callable(TestClassInSubPkg))

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
            pkg = importlib.__import__('pkg.submodule', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            TestClassInSubModule = pkg.submodule.TestClassInSubModule

            self.assertTrue(TestClassInSubModule is not None)
            self.assertTrue(callable(TestClassInSubModule))

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
            pkg = importlib.__import__('pkg.bytecode', globals=globals(),
                                         level=1)  # need globals to handle relative imports
            TestClassInBytecode = pkg.bytecode.TestClassInBytecode

            self.assertTrue(TestClassInBytecode is not None)
            self.assertTrue(callable(TestClassInBytecode))

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
            nspkg = importlib.__import__('nspkg.subpkg', globals=globals(), level=1)  # need globals to handle relative imports
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
            nspkg = importlib.__import__('nspkg.subpkg.submodule', globals=globals(), level=1)  # need globals to handle relative imports
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
            nspkg = importlib.__import__('nspkg.subpkg.bytecode', globals=globals(), level=1)  # need globals to handle relative imports
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
            nspkg = importlib.__import__('nspkg.subpkg', globals=globals(), level=1)  # need globals to handle relative imports
            TestClassInSubPkg = nspkg.subpkg.TestClassInSubPkg

            self.assertTrue(TestClassInSubPkg is not None)
            self.assertTrue(callable(TestClassInSubPkg))

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
            nspkg = importlib.__import__('nspkg.subpkg.submodule', globals=globals(), level=1)  # need globals to handle relative imports
            TestClassInSubModule = nspkg.subpkg.submodule.TestClassInSubModule

            self.assertTrue(TestClassInSubModule is not None)
            self.assertTrue(callable(TestClassInSubModule))

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
            TestClassInBytecode = nspkg.subpkg.bytecode.TestClassInBytecode

            self.assertTrue(TestClassInBytecode is not None)
            self.assertTrue(callable(TestClassInBytecode))

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

        # Using find_loader and load_module
        # TODO : pkg
        def test_importlib_loadmodule_ns_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # Verify that files exists and are dynamically importable
            # but namespace packages do not have loaders
            pkg = sys.modules.get(__package__)
            with self.assertRaises(ImportError):
                # not sure of the proper way to do relative import in that case
                importlib.find_loader(__package__ + '.nspkg', pkg.__path__)

            # Note : We are not testing the deprecated find_loader and load_module method,
            # since it is not clear if we are at all able to import a relative namespace package
            # since a namespace package has no loader

        # using find_spec and module_from_spec
        # TODO:  pkg
        def test_importlib_findspec_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

            self.assertTrue(subpkg is not None)
            self.assertTrue(subpkg.TestClassInSubPkg is not None)
            self.assertTrue(callable(subpkg.TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(subpkg)
            else:
                pass

        def test_importlib_findspec_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
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
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(submodule)
            else:
                pass

        def test_importlib_findspec_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

            # bytecode is not imported hwen executing the __init__ module, so we need to import it separately here
            bytecode_spec = importlib.util.find_spec('.nspkg.subpkg.bytecode', __package__)
            bytecode = importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we do this for a normal package
                bytecode_spec.loader.exec_module(bytecode)

            self.assertTrue(bytecode is not None)
            self.assertTrue(bytecode.TestClassInBytecode is not None)
            self.assertTrue(callable(bytecode.TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(bytecode)
            else:
                pass

        def test_importlib_findspec_class_from_relative_ns_subpkg(self):
            """Verify that message class is importable relatively"""
            print_importers()
            assert __package__

            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

            TestClassInSubPkg = subpkg.TestClassInSubPkg

            self.assertTrue(TestClassInSubPkg is not None)
            self.assertTrue(callable(TestClassInSubPkg))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_findspec_class_from_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

            # here we should get the module that has already be loaded while executing subpkg
            submodule = sys.modules.get(__package__ + '.nspkg.subpkg.submodule')

            TestClassInSubModule = submodule.TestClassInSubModule

            self.assertTrue(TestClassInSubModule is not None)
            self.assertTrue(callable(TestClassInSubModule))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_findspec_class_from_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
            nspkg = importlib.util.module_from_spec(nspkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(nspkg.__name__, nspkg)
            if nspkg_spec.loader:
                # we don't do this for a namespace package
                nspkg_spec.loader.exec_module(nspkg)

            subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
            subpkg = importlib.util.module_from_spec(subpkg_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(subpkg.__name__, subpkg)
            if subpkg_spec.loader:
                # we do this for a normal package
                subpkg_spec.loader.exec_module(subpkg)

            bytecode_spec = importlib.util.find_spec('.nspkg.subpkg.bytecode', __package__)
            bytecode = importlib.util.module_from_spec(bytecode_spec)
            # safely adding to sysmodules to be able to perform relative imports in there
            sys.modules.setdefault(bytecode.__name__, bytecode)
            if bytecode_spec.loader:
                # we do this for a normal package
                bytecode_spec.loader.exec_module(bytecode)

            TestClassInBytecode = bytecode.TestClassInBytecode

            self.assertTrue(TestClassInBytecode is not None)
            self.assertTrue(callable(TestClassInBytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_findspec_relative_nonnspkg_returns_None(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            assert importlib.util.find_spec('.bad_nspkg', __package__) is None





        # Using import_module
        # TODO pkg
        def test_importlib_importmodule_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__
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
                importlib.import_module('.bad_nspkg.bad_subpkg', package=__package__)


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

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_relative_ns_subpkg()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_relative_ns_subpkg_submodule()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_relative_ns_subpkg_bytecode()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_class_from_relative_ns_subpkg()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_class_from_relative_ns_subpkg_submodule()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_class_from_relative_ns_subpkg_bytecode()

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_import_relative_nonnspkg_raises()

    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_ns_raises(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_loadmodule_ns_raises()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_relative_ns_subpkg()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_relative_ns_subpkg_submodule()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_relative_ns_subpkg_bytecode()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_class_from_relative_ns_subpkg()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_class_from_relative_ns_subpkg_submodule()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode()

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute import_module")
    def test_importlib_importmodule_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceRaw, self).test_importlib_importmodule_relative_nonnspkg_raises()


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

    def test_importlib_import_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_relative_ns_subpkg()

    def test_importlib_import_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_relative_ns_subpkg_submodule()

    def test_importlib_import_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_relative_ns_subpkg_bytecode()

    def test_importlib_import_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_class_from_relative_ns_subpkg()

    def test_importlib_import_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_class_from_relative_ns_subpkg_submodule()

    def test_importlib_import_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_class_from_relative_ns_subpkg_bytecode()

    def test_importlib_import_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_import_relative_nonnspkg_raises()

    def test_importlib_loadmodule_ns_raises(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_loadmodule_ns_raises()

    def test_importlib_importmodule_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_relative_ns_subpkg()

    def test_importlib_importmodule_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_relative_ns_subpkg_submodule()

    def test_importlib_importmodule_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_relative_ns_subpkg_bytecode()

    def test_importlib_importmodule_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_class_from_relative_ns_subpkg()

    def test_importlib_importmodule_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_class_from_relative_ns_subpkg_submodule()

    def test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_class_from_relative_ns_subpkg_bytecode()

    def test_importlib_importmodule_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceFF2, self).test_importlib_importmodule_relative_nonnspkg_raises()


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
