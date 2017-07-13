from __future__ import absolute_import, print_function

import codecs

import marshal

import six

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
    import re

    # From IPython.utils.openpy
    try:
        from tokenize import detect_encoding
    except ImportError:
        from codecs import lookup, BOM_UTF8

        # things we rely on and need to put it in cache early, to avoid recursing.
        import encodings.ascii

        cookie_re = re.compile(r"coding[:=]\s*([-\w.]+)", re.UNICODE)
        cookie_comment_re = re.compile(r"^\s*#.*coding[:=]\s*([-\w.]+)", re.UNICODE)

        # Copied from Python 3.2 tokenize
        def _get_normal_name(orig_enc):
            """Imitates get_normal_name in tokenizer.c."""
            # Only care about the first 12 characters.
            enc = orig_enc[:12].lower().replace("_", "-")
            if enc == "utf-8" or enc.startswith("utf-8-"):
                return "utf-8"
            if enc in ("latin-1", "iso-8859-1", "iso-latin-1") or \
                    enc.startswith(("latin-1-", "iso-8859-1-", "iso-latin-1-")):
                return "iso-8859-1"
            return orig_enc


        # Copied from Python 3.2 tokenize
        def detect_encoding(readline):
            """
            The detect_encoding() function is used to detect the encoding that should
            be used to decode a Python source file.  It requires one argment, readline,
            in the same way as the tokenize() generator.
            It will call readline a maximum of twice, and return the encoding used
            (as a string) and a list of any lines (left as bytes) it has read in.
            It detects the encoding from the presence of a utf-8 bom or an encoding
            cookie as specified in pep-0263.  If both a bom and a cookie are present,
            but disagree, a SyntaxError will be raised.  If the encoding cookie is an
            invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
            'utf-8-sig' is returned.
            If no encoding is specified, then the default of 'utf-8' will be returned.
            """
            bom_found = False
            encoding = None
            default = 'utf-8'

            def read_or_stop():
                try:
                    return readline()
                except StopIteration:
                    return b''

            def find_cookie(line):
                try:
                    line_string = line.decode('ascii')
                except UnicodeDecodeError:
                    return None

                matches = cookie_re.findall(line_string)
                if not matches:
                    return None
                encoding = _get_normal_name(matches[0])
                try:
                    codec = lookup(encoding)
                except LookupError:
                    # This behaviour mimics the Python interpreter
                    raise SyntaxError("unknown encoding: " + encoding)

                if bom_found:
                    if codec.name != 'utf-8':
                        # This behaviour mimics the Python interpreter
                        raise SyntaxError('encoding problem: utf-8')
                    encoding += '-sig'
                return encoding

            first = read_or_stop()
            if first.startswith(BOM_UTF8):
                bom_found = True
                first = first[3:]
                default = 'utf-8-sig'
            if not first:
                return default, []

            encoding = find_cookie(first)
            if encoding:
                return encoding, [first]

            second = read_or_stop()
            if not second:
                return default, [first]

            encoding = find_cookie(second)
            if encoding:
                return encoding, [first, second]

            return default, [first, second]


    def strip_encoding_cookie(filelike):
        """Generator to pull lines from a text-mode file, skipping the encoding
        cookie if it is found in the first two lines.
        """
        it = iter(filelike)
        try:
            first = next(it)
            if not cookie_comment_re.match(first):
                yield first
            second = next(it)
            if not cookie_comment_re.match(second):
                yield second
        except StopIteration:
            return

        for line in it:
            yield line


    def source_to_unicode(txt, errors='replace', skip_encoding_cookie=True):
        """Converts a bytes string with python source code to unicode.
        Unicode strings are passed through unchanged. Byte strings are checked
        for the python source file encoding cookie to determine encoding.
        txt can be either a bytes buffer or a string containing the source
        code.
        """
        if isinstance(txt, six.text_type):
            return txt
        if isinstance(txt, six.binary_type):
            buffer = io.BytesIO(txt)
        else:
            buffer = txt
        try:
            encoding, _ = detect_encoding(buffer.readline)
        except SyntaxError:
            encoding = "ascii"
        buffer.seek(0)

        newline_decoder = io.IncrementalNewlineDecoder(None, True)

        text = io.TextIOWrapper(buffer, encoding, errors=errors, line_buffering=True)
        text.mode = 'r'
        if skip_encoding_cookie:
            return u"".join(strip_encoding_cookie(text))
        else:
            return text.read()

    def decode_source(source_bytes):
        """Decode bytes representing source code and return the string.
        Universal newline support is used in the decoding.
        """
        # source_bytes_readline = io.BytesIO(source_bytes).readline
        # encoding, _ = detect_encoding(source_bytes_readline)
        newline_decoder = io.IncrementalNewlineDecoder(None, True)
        return newline_decoder.decode(source_to_unicode(source_bytes))

    class Loader2(object):
        """Base class of common code needed by SourceFileLoader2, NamespaceLoader2 and ImpLoader."""

        def __init__(self, fullname, path=None):
            self.name = fullname
            # to get the same API as py3 Loader
            self.path = os.path.dirname(path) if path.endswith('__init__.py') else path

        def __eq__(self, other):
            return (self.__class__ == other.__class__ and
                    self.__dict__ == other.__dict__)

        def __hash__(self):
            return hash(self.name) ^ hash(self.path)

        def is_package(self, fullname):
            # in case of package we have to always have the directory as self.path
            # CAREFUL : This is a different logic than importlib, to also support namespaces.
            return os.path.isdir(self.path)

        def get_filename(self, fullname):
            raise NotImplemented

        def get_code(self, fullname):
            raise NotImplemented

        def exec_module(self, module):
            """Execute the module."""
            code = self.get_code(module.__name__)
            if code is None:
                raise ImportError('cannot load module {!r} when get_code() '
                                  'returns None'.format(module.__name__))

            exec(code, module.__dict__)

        def load_module(self, name):
            """Load a module from a file.
            """
            # Implementation inspired from pytest.rewrite and importlib

            # If there is an existing module object named 'name' in
            # sys.modules, the loader must use that existing module. (Otherwise,
            # the reload() builtin will not work correctly.)
            if name in sys.modules:
                return sys.modules[name]

            # I wish I could just call imp.load_compiled here, but __file__ has to
            # be set properly. In Python 3.2+, this all would be handled correctly
            # by load_compiled.
            mod = sys.modules.setdefault(name, imp.new_module(name))
            try:
                # Set a few properties required by PEP 302
                mod.__file__ = self.get_filename(name)
                # this will set mod.__repr__ to not builtin...
                mod.__loader__ = self
                if self.is_package(name):
                    mod.__path__ = [self.path]
                    mod.__package__ = name  # PEP 366
                else:
                    mod.__package__ = '.'.join(name.split('.')[:-1])  # PEP 366
                # if we want to skip compilation - useful for debugging
                # source = self.get_source(name)
                # exec(source, mod.__dict__)
                self.exec_module(mod)

            except:
                if name in sys.modules:
                    del sys.modules[name]
                raise
            return sys.modules[name]

    # inspired from importlib
    class NamespaceLoader2(Loader2):
        """
        Loader for (Implicit) Namespace Package, inspired from importlib.
        """
        def __init__(self, name, path=None):
            if not os.path.isdir(path):
                raise _ImportError("cannot be a namespace package", path=path)

            super(NamespaceLoader2, self).__init__(name, path)

        def load_module(self, name):
            """Load a module from a file.
            """
            mod = super(NamespaceLoader2, self).load_module(name)
            # this will change mod.__repr__ to get rid of (builtin)...

            return mod

        def is_package(self, fullname):
            return True

        def get_filename(self, fullname):
            """Return the path directly, is the matching directory"""
            return self.path

        def get_source(self, name):
            # Better to not rely on anyone (pkg_resources/pkgutil) for this, since it seems we can...
            return ''

        def get_code(self, fullname):
            return compile('', '<string>', 'exec', dont_inherit=True)

    # inspired from importlib2
    class SourceFileLoader2(Loader2):
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
            If it is a package the path must point to a directory.
            Otherwise the path to the python module is needed
            """
            super(SourceFileLoader2, self).__init__(fullname, path)

        def get_filename(self, fullname):
            """Return the path to the source file."""
            if os.path.isdir(self.path) and os.path.isfile(os.path.join(self.path, '__init__.py')):
                # to be compatible with usual loaders for python package, we return path to __init__.py
                return os.path.join(self.path, '__init__.py')
            else:
                return self.path  # module case

        def get_source(self, name):
            """Concrete implementation of InspectLoader.get_source."""
            path = self.get_filename(name)
            try:
                source_bytes = self.get_data(path)
            except OSError as exc:
                e = _ImportError('source not available through get_data()',
                                 name=name)
                e.__cause__ = exc
                raise e
            return decode_source(source_bytes)

        def get_code(self, fullname):
            source = self.get_source(fullname)
            _verbose_message('compiling code for "{0}"'.format(fullname))
            try:
                code = compile(source, self.get_filename(fullname), 'exec', dont_inherit=True)
                return code
            except TypeError:
                raise

        def get_data(self, path):
            """Return the data from path as raw bytes.
            """
            with io.FileIO(path, 'r') as file:
                return file.read()

    class ImpLoader(Loader2):
        """An Import Loader for python 2.7 using imp module"""

        def load_module(self, name):
            """Load a module from a file.
            """
            # Implementation inspired from pytest.rewrite and importlib

            # If there is an existing module object named 'name' in
            # sys.modules, the loader must use that existing module. (Otherwise,
            # the reload() builtin will not work correctly.)
            if name in sys.modules:
                return sys.modules[name]
            try:
                # we have already done the search, an gone through package layers
                # so we directly feed the latest module and correct path
                # to reuse the logic for choosing the proper loading behavior

                for name_idx, name_part in enumerate(name.split('.')):
                    pkgname = ".".join(name.split('.')[:name_idx+1])
                    if pkgname not in sys.modules:
                        path = None

                        if '.' in pkgname:
                            # parent has to be in sys.modules. make sure it is a package, else fails
                            if '__path__' in vars(sys.modules[pkgname.rpartition('.')[0]]):
                                path = sys.modules[pkgname.rpartition('.')[0]].__path__
                            else:
                                raise ImportError("{0} is not a package (no __path__ detected)".format(pkgname.rpartition('.')[0]))
                        else:  # using __file__ instead. should always be there.
                            path = sys.modules[pkgname].__file__ if pkgname in sys.modules else None
                        try:
                            file, pathname, description = imp.find_module(pkgname.rpartition('.')[-1], path)
                            sys.modules[pkgname] = imp.load_module(pkgname, file, pathname, description)
                        finally:
                            if file:
                                file.close()
            except:
                # dont pollute the interpreter environment if we dont know what we are doing
                if name in sys.modules:
                    del sys.modules[name]
                raise
            return sys.modules[name]
