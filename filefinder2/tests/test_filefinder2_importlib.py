from __future__ import absolute_import, print_function
"""
Testing import statement with filefinder2
"""

import sys
import unittest
import pytest  # we need to use pytest marker to get __package__ to get the proper value, making relative import works
import importlib

import filefinder2


# importlib
# https://pymotw.com/3/importlib/index.html
# https://pymotw.com/2/importlib/index.html

#
# Note : we cannot assume anything about import implementation (different python version, different version of pytest)
# => we need to test them all...
#

def print_importers():
    import sys
    import pprint

    print('PATH:'),
    pprint.pprint(sys.path)
    print()
    print('IMPORTERS:')
    for name, cache_value in sys.path_importer_cache.items():
        name = name.replace(sys.prefix, '...')
        print('%s: %r' % (name, cache_value))


# # This is useful since if we need relative imports here. Ref : http://stackoverflow.com/a/28154841/4006172
# # declaring __package__ if needed (this module is run individually)
# if __package__ is None and not __name__.startswith('filefinder2.tests.'):
#     import os
#     import sys
#     # from pathlib2 import Path
#     # top = Path(__file__).resolve().parents[2]
#     # Or
#     from os.path import abspath, dirname
#     top = abspath(__file__)
#     for _ in range(3):
#         top = dirname(top)
#
#     if sys.path[0] == os.path.dirname(__file__):
#         sys.path[0] = str(
#             top)  # we replace first path in list (current module dir path) by the path of the package.
#         # this avoid unintentional relative import (even without point notation).
#     else:  # not sure in which case this could happen, but just in case we don't want to break stuff
#         sys.path.append(str(top))
#
#     if __name__ == '__main__':
#         __name__ = '__init__'
#
#     __package__ = 'filefinder2.tests'
#     # Note we do NOT want to import everything in filefinder2 in this case


# We need to test implicit namespace packages PEP 420 (especially for python 2.7)
# Since we rely on it for ros import.
# But we can only test relative package structure
# TODO : depending on the python version we aim to support, we might be able to drop some tests here...
class TestImplicitNamespace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # This should activate only for old python
        filefinder2.activate()
        # python3 implicit namespaces should work out of the box.

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.__import__('.nspkg.subpkg')
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

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.__import__('.nspkg.subpkg.submodule')
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

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.__import__('.nspkg.subpkg.TestClassInSubPkg')
        TestClassInSubPkg = nspkg.subpkg.TestClassInSubPkg

        self.assertTrue(TestClassInSubPkg is not None)
        self.assertTrue(callable(TestClassInSubPkg))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(nspkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.__import__('.nspkg.subpkg.submodule.TestClassInSubModule')
        TestClassInSubModule = nspkg.subpkg.TestClassInSubModule

        self.assertTrue(TestClassInSubModule is not None)
        self.assertTrue(callable(TestClassInSubModule))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(nspkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, '__import__'), reason="importlib does not have attribute __import__")
    def test_importlib_import_relative_nonnspkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        with self.assertRaises(ImportError):
            importlib.__import__('.bad_nspkg.bad_subpkg', package=__package__)


    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        # Verify that files exists and are dynamically importable
        pkg_list = '.nspkg.subpkg'.split('.')[:-1]
        mod_list = '.nspkg.subpkg'.split('.')[1:]
        pkg = None
        for pkg_name, mod_name in zip(pkg_list, mod_list):
            pkg_loader = importlib.find_loader(pkg_name, pkg.__path__ if pkg else None)
            pkg = pkg_loader.load_module(mod_name)

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

    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # Verify that files exists and are dynamically importable
        pkg_list = '.nspkg.subpkg.submodule'.split('.')[:-1]
        mod_list = '.nspkg.subpkg.submodule'.split('.')[1:]
        pkg = None
        for pkg_name, mod_name in zip(pkg_list, mod_list):
            pkg_loader = importlib.find_loader(pkg_name, pkg.__path__ if pkg else None)
            pkg = pkg_loader.load_module(mod_name)

        test_mod = pkg

        self.assertTrue(test_mod is not None)
        self.assertTrue(test_mod.TestClassInSubModule is not None)
        self.assertTrue(callable(test_mod.TestClassInSubModule))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(test_mod)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__

        # Verify that files exists and are dynamically importable
        pkg_list = '.nspkg.subpkg.TestClassInSubPkg'.split('.')[:-1]
        mod_list = '.nspkg.subpkg.TestClassInSubPkg'.split('.')[1:]
        pkg = None
        for pkg_name, mod_name in zip(pkg_list, mod_list):
            pkg_loader = importlib.find_loader(pkg_name, pkg.__path__ if pkg else None)
            pkg = pkg_loader.load_module(mod_name)

        TestClassInSubPkg = pkg

        self.assertTrue(TestClassInSubPkg is not None)
        self.assertTrue(callable(TestClassInSubPkg))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(pkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        # Verify that files exists and are dynamically importable
        pkg_list = '.nspkg.subpkg.submodule.TestClassInSubModule'.split('.')[:-1]
        mod_list = '.nspkg.subpkg.submodule.TestClassInSubModule'.split('.')[1:]
        pkg = None
        for pkg_name, mod_name in zip(pkg_list, mod_list):
            pkg_loader = importlib.find_loader(pkg_name, pkg.__path__ if pkg else None)
            pkg = pkg_loader.load_module(mod_name)

        TestClassInSubModule = pkg

        self.assertTrue(TestClassInSubModule is not None)
        self.assertTrue(callable(TestClassInSubModule))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(pkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, 'find_loader') or not hasattr(importlib, 'load_module'),
                     reason="importlib does not have attribute find_loader or load_module")
    def test_importlib_loadmodule_relative_nonnspkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__

        with self.assertRaises(ImportError):
            importlib.load_module('.bad_nspkg.bad_subpkg', package=__package__)

    # TODO : dynamic using module_spec (python 3.5)

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute __import__")
    def test_importlib_importmodule_relative_ns_subpkg(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.import_module('.nspkg.subpkg', package=__package__)
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

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute __import__")
    def test_importlib_importmodule_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.import_module('.nspkg.subpkg.submodule', package=__package__)
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

    #@pytest.mark.skipif(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute __import__")
    def test_importlib_importmodule_class_from_relative_ns_subpkg(self):
        """Verify that message class is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.import_module('.nspkg.subpkg.TestClassInSubPkg', package=__package__)
        TestClassInSubPkg = nspkg.subpkg.TestClassInSubPkg

        self.assertTrue(TestClassInSubPkg is not None)
        self.assertTrue(callable(TestClassInSubPkg))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(nspkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute __import__")
    def test_importlib_importmodule_class_from_relative_ns_subpkg_submodule(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        nspkg = importlib.import_module('.nspkg.subpkg.submodule.TestClassInSubModule', package=__package__)
        TestClassInSubModule = nspkg.subpkg.TestClassInSubModule

        self.assertTrue(TestClassInSubModule is not None)
        self.assertTrue(callable(TestClassInSubModule))

        # TODO : implement some differences and check we get them...
        if hasattr(importlib, 'reload'):  # recent version of importlib
            # attempting to reload
            importlib.reload(nspkg)
        else:
            pass

    @unittest.skipIf(not hasattr(importlib, 'import_module'), reason="importlib does not have attribute __import__")
    def test_importlib_importmodule_relative_nonnspkg_raises(self):
        """Verify that package is importable relatively"""
        print_importers()
        assert __package__
        with self.assertRaises(ImportError):
            importlib.import_module('.bad_nspkg.bad_subpkg', package=__package__)


if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-x', __file__, '--boxed'])
