filefinder2
===========

`PEP420 <https://www.python.org/dev/peps/pep-0420/>`_ - Implicit Namespace Packages for Python 2.7

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - |travis| |requires| |landscape|
    * - Python
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://travis-ci.org/asmodehn/filefinder2.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/asmodehn/filefinder2

.. |requires| image:: https://requires.io/github/asmodehn/filefinder2/requirements.svg?branch=master
    :alt: Requirements Status
    :target: hhttps://requires.io/github/asmodehn/filefinder2/requirements/?branch=master

.. |landscape| image:: https://landscape.io/github/asmodehn/filefinder2/master/landscape.svg?style=flat
    :target: hhttps://landscape.io/github/asmodehn/filefinder2/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/filefinder2.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/filefinder2

.. |downloads| image:: https://img.shields.io/pypi/dm/filefinder2.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/filefinder2

.. |wheel| image:: https://img.shields.io/pypi/wheel/filefinder2.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/filefinder2

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/filefinder2.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/filefinder2

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/filefinder2.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/filefinder2

.. end-badges


filefinder2 implements PEP 420 in Python2, and make every directory a namespace package, effectively mimicking Python3 behavior.

To do this, filefinder2 includes finder and loader hooks that contain the implicit namespace logic.

It is worth noting that we achieve this without pkg_resources or pkgutil, minimizing the dependencies necessary for that feature.

Usage:
------
::

    import filefinder2

    with filefinder2.enable_pep420():
        import namespace.package



Also filefinder2 provides some of python3 importlib API, even without "activating" it.
For more details have a look inside the tests. There is a quite exhaustive usecase coverage.


Recent Upgrade Notes:
---------------------

filefinder2 until recently had an API with an implicit model::

    import filefinder2
    # just works !


because we were able to do things like::

    if sys.version_info < (3, 3):
        import filefinder2 as importlib
    else:
        import importlib

    # *should* just work for any python versions

However filefinder2 is not a standard library, and this model has proven to be quite tricky to use, given the little visibility an average developer has on the import sequence.
And as a general rule, it is better to remain in control of our import system, and know what you are doing.

Therefore it was recently changed to an explicit model (using a context manager class)::

    import filefinder2

    with filefinder2.Py3Importer():
        # works ! but doesn't change anything in python3

    # doesn't work any longer, if you are using python2


As a result, the check for the python interpreter version has been included inside filefinder2, instead of being expected of the user (which used to lead to tricks to install dependencies depending on version)
This means the above code will work and do what you expect it to, no matter the version of Python you are running.
