from __future__ import absolute_import, print_function

import codecs

import marshal

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

    from codecs import lookup, BOM_UTF8

    # From IPython.utils.openpy
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
        if isinstance(txt, unicode):  # unicode is the unicode type for py27
            return txt
        if isinstance(txt, str):
            buffer = io.BytesIO(txt)
        else:
            buffer = txt
        try:
            encoding, _ = detect_encoding(buffer.readline)
        except SyntaxError:
            encoding = "ascii"
        buffer.seek(0)
        text = io.TextIOWrapper(buffer, encoding, errors=errors, line_buffering=True)
        text.mode = 'r'
        if skip_encoding_cookie:
            return u"".join(strip_encoding_cookie(text))
        else:
            return text.read()

    class Loader2(object):
        """An abstract implementation of a Loader for py2.7"""
        def __init__(self, fullname, path=None):
            self.name = fullname
            self.path = path

        def __eq__(self, other):
            return (self.__class__ == other.__class__ and
                    self.__dict__ == other.__dict__)

        def __hash__(self):
            return hash(self.name) ^ hash(self.path)

        def get_code(self, fullname):
            source = self.get_source(fullname)
            _verbose_message('compiling code for "%s"' % fullname)
            try:
                code = compile(source, self.get_filename(fullname), 'exec', dont_inherit=True)
                return code
            except TypeError:
                raise

        def is_package(self, fullname):
            # in case of package we have to always have the directory as self.path
            return os.path.isdir(self.path)

        def get_filename(self, name):
            raise NotImplemented

        def get_data(self, path):
            raise NotImplemented

        def get_source(self, name):
            path = self.get_filename(name)
            try:
                source_bytes = self.get_data(path)
            except OSError as exc:
                e = _ImportError('source not available through get_data()',
                                 name=name)
                e.__cause__ = exc
                raise e

            # source_bytes_readline = io.BytesIO(source_bytes).readline
            # encoding = detect_encoding(source_bytes_readline)
            # newline_decoder = io.IncrementalNewlineDecoder(None, True)
            # return newline_decoder.decode(source_bytes.decode(encoding[0]))

            # return source_to_unicode(source_bytes)

            return source_bytes

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
                # source = self.get_source(name)
                # exec(source, mod.__dict__)
                exec(code, mod.__dict__)

            except:
                if name in sys.modules:
                    del sys.modules[name]
                raise
            return sys.modules[name]

    # inspired from importlib
    class NamespaceLoader2(Loader2):
        def __init__(self, name, path, path_finder=None):
            # self._path = _NamespacePath(name, path, path_finder)

            if not os.path.isdir(path):
                raise _ImportError("cannot be a namespace package", path=path)

            # Note for namespace package, we let pkg_resources/pkgutil manage the __path__ logic
            # Ref : https://packaging.python.org/guides/packaging-namespace-packages/
            # self._ns_impl = """__import__('pkg_resources').declare_namespace(__name__)"""
            # TODO : which one is best for us ?
            # self._ns_impl = """__path__ = __import__('pkgutil').extend_path(__path__, __name__)"""

            # Probably better to not rely on anyone for this if we can...
            # to not rely on complex APIs that have to support py2 + py3.
            # In our case relying on py3 API seems to be enough.
            self._ns_impl = ''

            super(NamespaceLoader2, self).__init__(name, path)

        @classmethod
        def module_repr(cls, module):
            """Return repr for the module.
            The method is deprecated.  The import machinery does the job itself.
            """
            return '<module {!r} (namespace)>'.format(module.__name__)

        def get_filename(self, fullname):
            """Return the path to the namespace directory."""
            return self.path

        def get_data(self, path):
            """Return the data from path as raw bytes.
            """
            # implicit namespace package via pkg_resources or pkgutil
            return self._ns_impl

    # inspired from importlib2
    class FileLoader2(Loader2):
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
            super(FileLoader2, self).__init__(fullname, path)

        def get_filename(self, fullname):
            """Return the path to the source file."""
            if os.path.isdir(self.path) and os.path.isfile(os.path.join(self.path, '__init__.py')):
                return os.path.join(self.path, '__init__.py')  # python package
            else:
                return self.path  # module case

        def is_package(self, fullname):
            # in case of package we have to always have the directory as self.path
            # we can always compute init path dynamically when needed.
            return os.path.isdir(self.path)

        def get_data(self, path):
            """Return the data from path as raw bytes.
            """
            with io.FileIO(path, 'r') as file:
                return file.read()

    # from importlib py36
    MAGIC_NUMBER = imp.get_magic()

    def _w_long(x):
        """Convert a 32-bit integer to little-endian."""
        return (int(x) & 0xFFFFFFFF).to_bytes(4, 'little')


    def _r_long(int_bytes):
        """Convert 4 bytes in little-endian to an integer."""
        return int.from_bytes(int_bytes, 'little')

    _code_type = type(_r_long.__code__)

    def _validate_bytecode_header(data, source_stats=None, name=None, path=None):
        """Validate the header of the passed-in bytecode against source_stats (if
        given) and returning the bytecode that can be compiled by compile().
        All other arguments are used to enhance error reporting.
        ImportError is raised when the magic number is incorrect or the bytecode is
        found to be stale. EOFError is raised when the data is found to be
        truncated.
        """
        exc_details = {}
        if name is not None:
            exc_details['name'] = name
        else:
            # To prevent having to make all messages have a conditional name.
            name = '<bytecode>'
        if path is not None:
            exc_details['path'] = path
        magic = data[:4]
        raw_timestamp = data[4:8]
        raw_size = data[8:12]
        if magic != MAGIC_NUMBER:
            message = 'bad magic number in {!r}: {!r}'.format(name, magic)
            _verbose_message('{}', message)
            raise ImportError(message, **exc_details)
        elif len(raw_timestamp) != 4:
            message = 'reached EOF while reading timestamp in {!r}'.format(name)
            _verbose_message('{}', message)
            raise EOFError(message)
        elif len(raw_size) != 4:
            message = 'reached EOF while reading size of source in {!r}'.format(name)
            _verbose_message('{}', message)
            raise EOFError(message)
        if source_stats is not None:
            try:
                source_mtime = int(source_stats['mtime'])
            except KeyError:
                pass
            else:
                if _r_long(raw_timestamp) != source_mtime:
                    message = 'bytecode is stale for {!r}'.format(name)
                    _verbose_message('{}', message)
                    raise ImportError(message, **exc_details)
            try:
                source_size = source_stats['size'] & 0xFFFFFFFF
            except KeyError:
                pass
            else:
                if _r_long(raw_size) != source_size:
                    raise ImportError('bytecode is stale for {!r}'.format(name),
                                      **exc_details)
        return data[12:]


    def _compile_bytecode(data, name=None, bytecode_path=None, source_path=None):
        """Compile bytecode as returned by _validate_bytecode_header()."""
        code = marshal.loads(data)
        if isinstance(code, _code_type):
            _verbose_message('code object from {!r}', bytecode_path)
            if source_path is not None:
                imp._fix_co_filename(code, source_path)
            return code
        else:
            raise ImportError('Non-code object in {!r}'.format(bytecode_path),
                              name=name, path=bytecode_path)


    class SourcelessFileLoader2(FileLoader2):

        def get_code(self, fullname):
            path = self.get_filename(fullname)
            data = self.get_data(path)
            bytes_data = _validate_bytecode_header(data, name=fullname, path=path)
            return _compile_bytecode(bytes_data, name=fullname, bytecode_path=path)

        def get_source(self, name):
            """Return None as there is no source code."""
            return None

    class ImpLoader(Loader2):
        """An Import Loader for python 2.7 using imp module"""

        def get_filename(self, fullname):
            """Return the path to the source file."""
            return self.path  # module case

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
                        # parent has to be in sys.modules. make sure it is a package, else fails
                        if '.' in pkgname and '__path__' in vars(sys.modules[pkgname.rpartition('.')[0]]):
                            path = sys.modules[pkgname.rpartition('.')[0]].__path__
                        else:
                            raise ImportError("{0} is not a package (no __path__ detected)".format(pkgname.rpartition('.')[0]))
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
