#! /usr/bin/python
import sys
from impl.files_finders import FolderTestFinder
from impl.runners import TestRunner
from impl.configuration import FileConfiguration
from impl.java import JavaClassGenerator, JavaFileCompiler

if __name__ == "__main__":
    configuration = FileConfiguration(os.path.join(os.paht.split(__file__)[0], "config.ini"))
    executor = TestExecutor(
        [JavaFileGenerator(configuration), 
         JavaFileCompiler(configuration), 
         JavaFileLauncher(configuration)])
    runner = TestRunner(FolderTestFinder(sys.argv), executor)
    runner.run()