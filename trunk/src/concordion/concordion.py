#!/usr/bin/python

import threading
import os, sys
import SimpleXMLRPCServer
import popen2
from impl.java import JavaClassGenerator


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

def load_config(config_dir):
    result = {}
    execfile(os.path.join(config_dir, "config.ini"), result)
    return result

def main(the_class, the_file):
    installation_path = os.path.split(__file__)[0]
    config = load_config(installation_path)
    lib_path = os.path.join(installation_path, "lib")
    instance = the_class()
    java_filename = the_file.replace(".py", ".java")
    java_directory = os.path.split(the_file)[0]
    java_classname = os.path.basename(java_filename).replace(".java", "")
    
    java_fixture = open(java_filename, "w")
    java_fixture.write(JavaClassGenerator(instance, config['server_port']).generate())
    java_fixture.close()
    
    xmlRpcServer = XMLRPCServer(instance, config['server_port'])
    thread = threading.Thread(target=xmlRpcServer)
    thread.setDaemon(True)
    thread.start()

    jars = [
            "concordion-1.2.0.jar",
            "junit-3.8.2.jar",
            "junit-4.4.jar",
            "xmlrpc-client-3.1.jar",
            "xmlrpc-common-3.1.jar",
            "xom-1.1.jar",
            "ws-commons-util-1.0.2.jar",
            "ognl-2.6.9.jar"
    ]
    classpath = ""
    for jar in jars:
        classpath += os.path.join(lib_path, jar) + ":"
    classpath += java_directory

    execute_command(config['javac_command'] + " -cp " + classpath + " " + java_filename)
    
    java_class_filename = java_filename.replace(".java", "")
    returned_code = execute_command(config['java_command'] + 
                                    " -Dconcordion.output.dir="+ config['output_folder'] +
                                    " -cp " + classpath + " org.junit.runner.JUnitCore " + java_classname,
                                    True)
    os.remove(java_filename)
    os.remove(java_filename.replace('.java', '.class'))
    if returned_code != 0 :
        sys.exit(1)
