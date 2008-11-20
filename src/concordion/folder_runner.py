#! /usr/bin/python
from impl.files_finders import FolderTestFinder
from impl.runners import TestRunner

if __name__ == "__main__":
    executor = TestExecutor([JavaFileGenerator(), JavaFileCompiler(), JavaFileLauncher()])
    runner = TestRunner(FolderTestFinder(args), executor)
    runner.run()