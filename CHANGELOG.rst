Changelog
=========


0.3.1 (2017-07-03)
------------------
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


