#! /usr/bin/python
import sys
from impl.files_finders import FolderTestFinder
from impl.runners import TestRunner
from impl.configuration import FileConfiguration
from impl.java import JavaClassGenerator, JavaFileCompiler, Classpath

if __name__ == "__main__":
    this_dir = os.path.split(__file__)[0]
    configuration = FileConfiguration(os.path.join(this_dir, "config.ini"))
    classpath = Classpath(os.path.join(this_dir, "lib"))
    executor = TestExecutor(
        [JavaFileGenerator(configuration), 
         JavaFileCompiler(configuration, classpath), 
         JavaFileLauncher(configuration, classpath)])
    runner = TestRunner(FolderTestFinder(sys.argv), executor)
    runner.run()