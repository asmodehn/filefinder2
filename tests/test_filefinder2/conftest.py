"""
Configuration module allowing to run :
- relevant tests without importing filefinder2, to make sure the tests make sense in a usual python2 or python3 context
- relevant tests without filefinder2 activated, to make sure filefinder2 import doesnt break any python2 or python3 expectation
- all filefinder2 tests to make sure filefinder2 works as python3 would, on python2 and python3.

"""
import pytest


def pytest_addoption(parser):
    # options available only on python3
    parser.addoption("--noff2", action="store_true",
                     help="filefinder is not imported. we will test the pure python import behavior.")

    # options available on all pythons
    parser.addoption("--noactive", action="store_true",
                     help="filefinder is imported but not activated")


@pytest.fixture(scope="class")
def importlib(request):
    """
    Stores an importlib in the current test class,
      and returns an active importer instance supporting namespaces (PEP420).
    The stores importlib is importlib in python3 or if --noff2 is specified,
      otherwise importlib is filefinder2
    An instance of filefinder2.Py3Importer is added to the class as "importer" member
      if the importeris active (that is if --noactive is not specified)
    """

    if request.config.getoption("--noff2", False):
        # we want to check that filefinder2 provide similar API as importlib
        import importlib
        # https://pymotw.com/3/importlib/index.html
        # https://pymotw.com/2/importlib/index.html
        request.cls.importlib = importlib
        importer_instance = None
    else:
        print("noff2:{0}".format(request.config.getoption("--noff2")))
        import filefinder2
        request.cls.importlib = filefinder2

        # here we need to also test creation (but not activation) fo the importer
        importer_instance = filefinder2.Py3Importer()

        if not request.config.getoption("--noactive", False):
            # calling enter and exit manually here to workaround pytest yield fixture limitations
            importer_instance.__enter__()


    # Note : filefinder2 will also be used with python3,
    # but it should do the usual python3 thing, and if necessary use importlib internally.
    yield importer_instance

    if importer_instance is not None:
         importer_instance.__exit__(None, None, None)
