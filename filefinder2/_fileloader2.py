from __future__ import absolute_import

"""
A module to load python file, but also embedding namespace pacakge logic (PEP420), implemented via pkg_resources
"""

# We need to be extra careful with python versions
# Ref : https://docs.python.org/2/library/modules.html?highlight=imports
# Ref : https://docs.python.org/3/library/modules.html?highlight=imports
import os
import sys

from ._utils import _ImportError, _verbose_message

if (2, 7) <= sys.version_info < (3, 4):  # valid until which py3 version ?

    import io
    import errno
    import imp

    # inspired from importlib2
    class FileLoader2(object):
        """Base file loader class which implements the loader protocol methods that
        require file system usage. Also implements implicit namespace package PEP 420.

        CAREFUL: the finder/loader logic is DIFFERENT than for python3.
        A namespace package, or a normal package, need to return a directory path.
        get_filename() will append '__init__.py' if it exists and needs to be called when a module path is needed
        """

        def __init__(self, fullname, path):
            """Cache the module name and the path to the file found by the
            finder.
            :param fullname the name of the module to load
            :param path to the module or the package.
            If it is a package (namespace or not) the path must point to a directory.
            Otherwise the path to the python module is needed
            """
            self.name = fullname
            self.path = path
            # Note for namespace package, we let pkg_resources/pkgutil manage the __path__ logic
            # Ref : https://packaging.python.org/guides/packaging-namespace-packages/
            self._ns_impl = """__import__('pkg_resources').declare_namespace(__name__)"""
            # TODO : which one is best for us ?
            # self._ns_impl = """__path__ = __import__('pkgutil').extend_path(__path__, __name__)"""

        def __eq__(self, other):
            return (self.__class__ == other.__class__ and
                    self.__dict__ == other.__dict__)

        def __hash__(self):
            return hash(self.name) ^ hash(self.path)

        def get_source(self, fullname):
            """Concrete implementation of InspectLoader.get_source."""
            path = self.get_filename(fullname)
            try:
                source_bytes = self.get_data(path)
            except OSError as exc:
                e = _ImportError('source not available through get_data()',
                                 name=fullname)
                e.__cause__ = exc
                raise e
            return source_bytes
            # return decode_source(source_bytes)

        def load_module(self, name):
            """Load a module from a file.
            """
            # Implementation inspired from pytest.rewrite and importlib

            # If there is an existing module object named 'name' in
            # sys.modules, the loader must use that existing module. (Otherwise,
            # the reload() builtin will not work correctly.)
            if name in sys.modules:
                return sys.modules[name]

            code = self.get_code(name)
            if code is None:
                raise _ImportError('cannot load module when get_code() '
                                  'returns None', name=name)
            # I wish I could just call imp.load_compiled here, but __file__ has to
            # be set properly. In Python 3.2+, this all would be handled correctly
            # by load_compiled.
            mod = sys.modules.setdefault(name, imp.new_module(name))
            try:
                # Set a few properties required by PEP 302
                mod.__file__ = self.get_filename(name)
                mod.__loader__ = self
                if self.is_package(name):
                    mod.__path__ = [self.path]
                    mod.__package__ = name  # PEP 366
                else:
                    mod.__package__ = '.'.join(name.split('.')[:-1])  # PEP 366
                # if we want to skip compilation - useful for debugging
                source = self.get_source(name)
                exec (source, mod.__dict__)
                #exec(code, mod.__dict__)

            except:
                if name in sys.modules:
                    del sys.modules[name]
                raise
            return sys.modules[name]

        def get_filename(self, fullname):
            """Return the path to the source file."""
            if os.path.isdir(self.path) and os.path.isfile(os.path.join(self.path, '__init__.py')):
                return os.path.join(self.path, '__init__.py')  # python package
            else:
                return self.path  # module or namespace package case

        def get_code(self, fullname):
            source = self.get_source(fullname)
            _verbose_message('compiling code for "%s"' % fullname)
            return compile(source, self.get_filename(fullname), 'exec', dont_inherit=True)

        def is_package(self, fullname):
            # in case of package we have to always have the directory as self.path
            # we can always compute init path dynamically when needed.
            return os.path.isdir(self.path)

        def get_data(self, path):
            """Return the data from path as raw bytes.
            Implements PEP 420 using pkg_resources
            """
            try:
                with io.FileIO(path, 'r') as file:
                    return file.read()
            except IOError as ioe:
                if ioe.errno == errno.EISDIR:
                    # implicit namespace package via pkg_resources or pkgutil
                    return self._ns_impl
                else:
                    raise
