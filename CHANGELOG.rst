Changelog
=========


0.4.2 (2018-05-17)
------------------
- Merge pull request #38 from asmodehn/docs. [AlexV]

  adding generated doc
- Cleanup docs and fixing links. [AlexV]
- Small machinery cleanup. [AlexV]
- Merge pull request #39 from asmodehn/refactor_force. [AlexV]

  refactored a bit to be able to enforce using backported classes in py3
- Adding missing import. [AlexV]
- Reviewing hooks to make sure they come from machinery that manages
  py2/py3. [AlexV]
- Small fix after testing with rosimport on python3. [AlexV]
- Refactored a bit to be able to enforce using backported classes in
  python3. fixed an error where cache was not cleaned on activate on
  python3. [AlexV]
- Updated docs. [AlexV]
- Adding generated doc. [AlexV]
- Removed quantifiedCode badge. [AlexV]

  cleaning readme text.
- Update pytest from 3.1.3 to 3.5.0 (#36) [pyup.io bot]
- Merge pull request #35 from asmodehn/pyup-update-
  twine-1.9.1-to-1.11.0. [AlexV]

  Update twine to 1.11.0
- Update twine from 1.9.1 to 1.11.0. [pyup-bot]
- Fixing PEP link in README for good this time. [alexv]


0.4.1 (2017-08-08)
------------------
- V0.4.1. [alexv]
- Fixing PEP link in README. [alexv]
- Merge pull request #13 from asmodehn/pyup-update-pytest-
  xdist-1.18.1-to-1.18.2. [AlexV]

  Update pytest-xdist to 1.18.2
- Update pytest-xdist from 1.18.1 to 1.18.2. [pyup-bot]
- Restructuring tests. [alexv]
- Skipping tests if they are run in unboxed mode (and cannot test any
  import properly) [alexv]
- Merge pull request #12 from asmodehn/import_23_api. [AlexV]

  Import 23 api
- Fixing import order. [alexv]
- Cleanup and style changes. [alexv]
- Removing broken sourcelessfileloader. [alexv]
- Small fixes and separate tests with different ways to import with
  importlib, to not have one pollute the other if unboxed, given that
  one package should use only one way, made for one interpreter version.
  [alexv]
- ImpFileloader not using broken SourcelessFileLoader for now. [alexv]
- Refining activation / deactivation of filefinder2 FileFinder not
  raising ImportError on __init__ to match python3 behavior. [alexv]
- Implemented importlib API. All tests passing except exec_module on
  bytecode loader. [alexv]
- Fixing tests by fixing namespace package handling in pathfinder.
  [alexv]
- WIP refactoring to use filefinder2 as an API for cross py2 py3 custom
  importers. [alexv]
- Fixing __init__.py to expose our importer API. [alexv]
- Starting to wrap importlib useful api for custom importer... [alexv]


0.3.1 (2017-07-17)
------------------
- V0.3.1. [alexv]
- Preventing multiple activation to pollute sys.path_hooks and
  sys.meta_path. [alexv]
- Exposing path_hook only if python2. [alexv]
- Making ns_hook publish in case hte client wants to do a search on
  sys.path_hook. [alexv]
- Merge pull request #9 from asmodehn/pyup-pin-pytest-3.1.3. [AlexV]

  Pin pytest to latest version 3.1.3
- Merge branch 'master' into pyup-pin-pytest-3.1.3. [AlexV]
- Merge branch 'master' into pyup-pin-pytest-3.1.3. [AlexV]
- Merge pull request #8 from asmodehn/pyup-pin-twine-1.9.1. [AlexV]

  Pin twine to latest version 1.9.1
- Merge branch 'master' into pyup-pin-twine-1.9.1. [AlexV]
- Pin twine to latest version 1.9.1. [pyup-bot]
- Merge pull request #10 from asmodehn/pyup-pin-pytest-xdist-1.18.1.
  [AlexV]

  Pin pytest-xdist to latest version 1.18.1
- Pin pytest-xdist to latest version 1.18.1. [pyup-bot]
- Merge pull request #7 from asmodehn/pyup-pin-gitchangelog-3.0.3.
  [AlexV]

  Pin gitchangelog to latest version 3.0.3
- Pin gitchangelog to latest version 3.0.3. [pyup-bot]
- Pin pytest to latest version 3.1.3. [pyup-bot]
- Moving tests outside directory, to keep package code and dependencies
  minimal. [alexv]
- Exposing PathFinder2 to clients. [alexv]
- Extracting PathFinder2 from NamespaceMetaFinder2. [alexv]
- Merge pull request #6 from asmodehn/fixing_namespace_repr. [AlexV]

  override load_module in namespace loader to fix repr for namespace pa…
- Override load_module in namespace loader to fix repr for namespace
  package. [alexv]
- API compatibility with py3 FileLoader. [alexv]
- Fixing logic importing base modules from bytecode or extensions.
  [alexv]
- Merge pull request #5 from asmodehn/newline_encoding. [AlexV]

  Newline encoding
- Fixing a few QC issues. [alexv]
- Now handling encoding properly in SourceFileLoader. [alexv]
- Adding test for source file encoding. [alexv]
- Enabling newline encoding detection. [alexv]
- Merge pull request #4 from asmodehn/bytecode. [AlexV]

  Bytecode
- Now compiling to bytecode at the test setup phase. [alexv]
- Cleaning loader module. [alexv]
- Implemented imp based loader for bytecode on py27. all tests passing.
  [alexv]
- Added bytecode test. [alexv]
- Improved doc. [alexv]


0.2.1 (2017-07-03)
------------------
- Generating changelog and changing version. [alexv]
- Adding gitignore. [alexv]
- Added python 3.6 to tests. [alexv]
- Exposed loader classes. fixed finder __init__ check. [alexv]
- Moving namespace logic in meta_path hook. Splitted loader for
  namespace or actual file, to make extending it simpler. [alexv]
- Small change to make usage from another importer easier. [alexv]
- Adding classifiers. [alexv]
- Fixing ReST README. [AlexV]
- Fixes for release. [alexv]
- V0.1.1. [alexv]
- Adding badges. moving to rst README format. [alexv]
- Making tox happy for all tested python. [alexv]
- Getting all tests to pass for py2. [alexv]
- Dropping in first version of filefinder2. [alexv]
- Initial commit. [AlexV]


