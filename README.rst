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


