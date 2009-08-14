import os, sys
from impl.java import JavaClassGenerator, Classpath, JavaFileCompiler, JavaTestLauncher
from impl.configuration import FileConfiguration
from impl.executors import CommandExecutor
from impl.xmlrpc import XmlRpcServer
from impl.files_finders import FolderTestFinder


class FolderRunner:
    def run(self, directory):
        python_files = FolderTestFinder(directory).find_files()
        installation_path = os.path.split(__file__)[0]
        config = FileConfiguration(os.path.join(installation_path, "config.ini"))
        lib_path = os.path.join(installation_path, "lib")
        classpath = Classpath(lib_path)
        
        class_generator = JavaClassGenerator(directory, config)
        java_files = class_generator.run(python_files)
        java_suite = class_generator.suite(java_files)
        java_files.append(java_suite)
        
        executor = CommandExecutor()
        
        java_class_filenames = JavaFileCompiler(config, classpath, executor).compile(java_files)
        
        xmlRpcServer = XmlRpcServer(config, python_files)
        xmlRpcServer.launch()
       
        test_result = JavaTestLauncher(config, classpath, executor, directory).launch(java_suite.replace('.java', '.class'))
        xmlRpcServer.stop()
        
        for java_filename in java_files :
            os.remove(java_filename)
        for java_class_filename in java_class_filenames:
            os.remove(java_class_filename)
        
        sys.exit(test_result)