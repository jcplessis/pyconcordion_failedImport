#! /usr/bin/python
import sys
from impl.files_finders import FolderTestFinder
from impl.runners import TestRunner
from impl.java import JavaClassGenerator, JavaFileCompiler

if __name__ == "__main__":
    executor = TestExecutor([JavaFileGenerator(), JavaFileCompiler(), JavaFileLauncher()])
    runner = TestRunner(FolderTestFinder(sys.argv), executor)
    runner.run()