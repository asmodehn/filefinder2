from __future__ import absolute_import, print_function

import copy

"""
Testing rosmsg_import with import keyword.
CAREFUL : these tests should run with pytest --boxed in order to avoid polluting each other sys.modules
"""

import os
import sys
import unittest

# CAREFUL : it seems this does have side effect in pytest modules and hooks setup.
from ._utils import print_importers

# importlib
# https://pymotw.com/3/importlib/index.html
# https://pymotw.com/2/importlib/index.html


# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure
class WrapperToHideUnittestCase:
    class TestImplicitNamespace(unittest.TestCase):
        """
        Testing PEP 420
        """
        def test_import_relative_ns_subpkg(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg'))
            else:
                from .nspkg import subpkg as test_pkg

                self.assertTrue(test_pkg is not None)
                self.assertTrue(test_pkg.TestClassInSubPkg is not None)
                self.assertTrue(callable(test_pkg.TestClassInSubPkg))

        def test_import_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg'))
            else:
                from .nspkg.subpkg import submodule as test_mod

                self.assertTrue(test_mod is not None)
                self.assertTrue(test_mod.TestClassInSubModule is not None)
                self.assertTrue(callable(test_mod.TestClassInSubModule))

        def test_import_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg.bytecode'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg.bytecode'))
            else:
                from .nspkg.subpkg import bytecode as test_bc

                self.assertTrue(test_bc is not None)
                self.assertTrue(test_bc.TestClassInBytecode is not None)
                self.assertTrue(callable(test_bc.TestClassInBytecode))

        def test_import_class_from_relative_ns_subpkg(self):
            """Verify that message class is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg'))
            else:
                from .nspkg.subpkg import TestClassInSubPkg

                self.assertTrue(TestClassInSubPkg is not None)
                self.assertTrue(callable(TestClassInSubPkg))

        def test_import_class_from_relative_ns_subpkg_submodule(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg.submodule'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg.submodule'))
            else:
                from .nspkg.subpkg.submodule import TestClassInSubModule

                self.assertTrue(TestClassInSubModule is not None)
                self.assertTrue(callable(TestClassInSubModule))

        def test_import_class_from_relative_ns_subpkg_bytecode(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__

            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.nspkg.subpkg'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.nspkg.subpkg'))
            else:
                from .nspkg.subpkg.bytecode import TestClassInBytecode

                self.assertTrue(TestClassInBytecode is not None)
                self.assertTrue(callable(TestClassInBytecode))

        def test_import_relative_nonnspkg_raises(self):
            """Verify that package is importable relatively"""
            print_importers()
            assert __package__


            # import checks sys.modules by itself
            # but the test is not reflecting anything if we use the already loaded module.
            if sys.modules.get(__package__ + '.bad_nspkg'):
                raise unittest.SkipTest("module previously loaded".format(__package__ + '.bad_nspkg'))
            else:
                with self.assertRaises(ImportError):
                    from .bad_nspkg import bad_subpkg


class TestImplicitNamespaceRaw(WrapperToHideUnittestCase.TestImplicitNamespace):
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

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_import_relative_ns_subpkg()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_import_relative_ns_subpkg_submodule()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_import_relative_ns_subpkg_bytecode()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceRaw, self).test_import_class_from_relative_ns_subpkg()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceRaw, self).test_import_class_from_relative_ns_subpkg_submodule()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceRaw, self).test_import_class_from_relative_ns_subpkg_bytecode()

    @unittest.skipIf(sys.version_info < (3, 3), reason="python 2 does not support namespaces")
    def test_import_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceRaw, self).test_import_relative_nonnspkg_raises()


class TestImplicitNamespaceFF2(WrapperToHideUnittestCase.TestImplicitNamespace):
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

        import filefinder2
        filefinder2.activate()
        # Note : filefinder2 will also be used with python3, but it should internally use importlib.

    def test_import_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_import_relative_ns_subpkg()

    def test_import_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_import_relative_ns_subpkg_submodule()

    def test_import_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_import_relative_ns_subpkg_bytecode()

    def test_import_class_from_relative_ns_subpkg(self):
        super(TestImplicitNamespaceFF2, self).test_import_class_from_relative_ns_subpkg()

    def test_import_class_from_relative_ns_subpkg_submodule(self):
        super(TestImplicitNamespaceFF2, self).test_import_class_from_relative_ns_subpkg_submodule()

    def test_import_class_from_relative_ns_subpkg_bytecode(self):
        super(TestImplicitNamespaceFF2, self).test_import_class_from_relative_ns_subpkg_bytecode()

    def test_import_relative_nonnspkg_raises(self):
        super(TestImplicitNamespaceFF2, self).test_import_relative_nonnspkg_raises()


# TODO  : test deriving an importer from filefinder2 to test the extension usage (like done in rosimporter)

if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
