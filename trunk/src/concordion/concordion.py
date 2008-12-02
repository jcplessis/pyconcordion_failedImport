#!/usr/bin/python

import threading
import os, sys
import SimpleXMLRPCServer
import popen2
from impl.java import JavaClassGenerator, Classpath, JavaFileCompiler
from impl.configuration import FileConfiguration
from impl.executors import CommandExecutor


class XMLRPCServer:
    def __init__(self, instance, port):
        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", port), logRequests=False)
        self.server.register_instance(instance)
        
    def __call__(self):
        self.server.serve_forever()


def main(the_class, the_file):
    installation_path = os.path.split(__file__)[0]
    config = FileConfiguration(os.path.join(installation_path, "config.ini"))
    lib_path = os.path.join(installation_path, "lib")
    

    java_filename = JavaClassGenerator().run([the_file])[0]
    java_classname = os.path.basename(java_filename).replace(".java", "")
    
    instance = the_class()
    xmlRpcServer = XMLRPCServer(instance, config.get('server_port'))
    thread = threading.Thread(target=xmlRpcServer)
    thread.setDaemon(True)
    thread.start()

    java_directory = os.path.split(the_file)[0]
    classpath = Classpath(lib_path)
    classpath.addDirectory(java_directory)

    executor = CommandExecutor()
    java_class_filename = JavaFileCompiler(config, classpath, executor).compile([java_filename])[0]
    
    returned_code = executor.run(config.get('java_command') + 
                                    " -Dconcordion.output.dir="+ config.get('output_folder') +
                                    " -cp " + classpath.getClasspath() + " junit.textui.TestRunner " + java_classname,
                                    True)
    os.remove(java_filename)
    os.remove(java_filename.replace('.java', '.class'))
    if returned_code != 0 :
        sys.exit(1)
