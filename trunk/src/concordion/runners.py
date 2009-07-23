import os, sys
from impl.java import JavaClassGenerator, Classpath, JavaFileCompiler, JavaTestLauncher
from impl.configuration import FileConfiguration
from impl.executors import CommandExecutor
from impl.xmlrpc import XmlRpcServer
from impl.launcher import TestLauncher
from impl.files_finders import FolderTestFinder


class FolderRunner:
    def run(self, directory):
        python_files = FolderTestFinder(directory).find_files()
        installation_path = os.path.split(__file__)[0]
        config = FileConfiguration(os.path.join(installation_path, "config.ini"))
        lib_path = os.path.join(installation_path, "lib")
        classpath = Classpath(lib_path)
        
        java_files = JavaClassGenerator(directory, config).run(python_files)
        
        executor = CommandExecutor()
        
        java_class_filenames = JavaFileCompiler(config, classpath, executor).compile(java_files)
        
        xmlRpcServer = XmlRpcServer(config, python_files)
        xmlRpcServer.launch()
        java_launcher = JavaTestLauncher(config, classpath, executor, directory)
        test_result = 0
        for java_class in java_class_filenames:
            test_result += java_launcher.launch(java_class)
        
        xmlRpcServer.stop()
        
        for java_filename in java_files :
            os.remove(java_filename)
        for java_class_filename in java_class_filenames:
            os.remove(java_class_filename)
        
        sys.exit(test_result)