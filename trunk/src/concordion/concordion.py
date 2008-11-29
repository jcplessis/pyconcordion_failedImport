#!/usr/bin/python

import threading
import os, sys
import SimpleXMLRPCServer
import popen2
from impl.java import JavaClassGenerator, Classpath
from impl.configuration import FileConfiguration


class XMLRPCServer:
    def __init__(self, instance, port):
        self.server = SimpleXMLRPCServer.SimpleXMLRPCServer(("localhost", port), logRequests=False)
        self.server.register_instance(instance)
        
    def __call__(self):
        self.server.serve_forever()

def execute_command(command, display_output=False):
    process =  popen2.Popen4(command)
    res = process.wait()
    if res != 0 or display_output: 
        for line in process.fromchild:
            print line,
    return res

def main(the_class, the_file):
    installation_path = os.path.split(__file__)[0]
    config = FileConfiguration(os.path.join(installation_path, "config.ini"))
    lib_path = os.path.join(installation_path, "lib")
    instance = the_class()
    

    java_filename = JavaClassGenerator().run([the_file])[0]
    java_classname = os.path.basename(java_filename).replace(".java", "")
    
    xmlRpcServer = XMLRPCServer(instance, config.get('server_port'))
    thread = threading.Thread(target=xmlRpcServer)
    thread.setDaemon(True)
    thread.start()

    java_directory = os.path.split(the_file)[0]
    classpath = Classpath(lib_path)
    classpath.addDirectory(java_directory)

    execute_command(config.get('javac_command') + " -cp " + classpath.getClasspath() + " " + java_filename)
    
    java_class_filename = java_filename.replace(".java", "")
    returned_code = execute_command(config.get('java_command') + 
                                    " -Dconcordion.output.dir="+ config.get('output_folder') +
                                    " -cp " + classpath.getClasspath() + " junit.textui.TestRunner " + java_classname,
                                    True)
    os.remove(java_filename)
    os.remove(java_filename.replace('.java', '.class'))
    if returned_code != 0 :
        sys.exit(1)
