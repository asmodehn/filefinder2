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

        # using find_spec and module_from_spec
        # TODO:  pkg
        def test_importlib_findspec_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
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

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
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

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
                subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
                subpkg = importlib.util.module_from_spec(subpkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(subpkg.__name__, subpkg)
                if subpkg_spec.loader:
                    # we do this for a normal package
                    subpkg_spec.loader.exec_module(subpkg)

            # we need to check sys.modules before doing anything
            bytecode = sys.modules.get(__package__ + '.nspkg.subpkg.bytecode')
            if not bytecode:
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

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
                subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
                subpkg = importlib.util.module_from_spec(subpkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(subpkg.__name__, subpkg)
                if subpkg_spec.loader:
                    # we do this for a normal package
                    subpkg_spec.loader.exec_module(subpkg)

            test_class_in_subpkg = subpkg.TestClassInSubPkg

            self.assertTrue(test_class_in_subpkg is not None)
            self.assertTrue(callable(test_class_in_subpkg))

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

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
                subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
                subpkg = importlib.util.module_from_spec(subpkg_spec)
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
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_findspec_class_from_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # we need to check sys.modules before doing anything
            nspkg = sys.modules.get(__package__ + '.nspkg')
            if not nspkg:
                nspkg_spec = importlib.util.find_spec('.nspkg', __package__)
                nspkg = importlib.util.module_from_spec(nspkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(nspkg.__name__, nspkg)
                if nspkg_spec.loader:
                    # we don't do this for a namespace package
                    nspkg_spec.loader.exec_module(nspkg)

            # we need to check sys.modules before doing anything
            subpkg = sys.modules.get(__package__ + '.nspkg.subpkg')
            if not subpkg:
                subpkg_spec = importlib.util.find_spec('.nspkg.subpkg', __package__)
                subpkg = importlib.util.module_from_spec(subpkg_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(subpkg.__name__, subpkg)
                if subpkg_spec.loader:
                    # we do this for a normal package
                    subpkg_spec.loader.exec_module(subpkg)

            # we need to check sys.modules before doing anything
            bytecode = sys.modules.get(__package__ + '.nspkg.subpkg.bytecode')
            if not bytecode:
                bytecode_spec = importlib.util.find_spec('.nspkg.subpkg.bytecode', __package__)
                bytecode = importlib.util.module_from_spec(bytecode_spec)
                # safely adding to sysmodules to be able to perform relative imports in there
                sys.modules.setdefault(bytecode.__name__, bytecode)
                if bytecode_spec.loader:
                    # we do this for a normal package
                    bytecode_spec.loader.exec_module(bytecode)

            test_class_in_bytecode = bytecode.TestClassInBytecode

            self.assertTrue(test_class_in_bytecode is not None)
            self.assertTrue(callable(test_class_in_bytecode))

            # TODO : implement some differences and check we get them...
            if hasattr(importlib, 'reload'):  # recent version of importlib
                # attempting to reload
                importlib.reload(nspkg)
            else:
                pass

        def test_importlib_findspec_relative_nonnspkg_returns_none(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            assert importlib.util.find_spec('.bad_nspkg', __package__) is None


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
