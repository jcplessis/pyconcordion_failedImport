#!/usr/bin/python

import threading
import os, sys
import SimpleXMLRPCServer
from impl.java import JavaClassGenerator, Classpath, JavaFileCompiler, JavaTestLauncher
from impl.configuration import FileConfiguration
from impl.executors import CommandExecutor
from impl.xmlrpc import XmlRpcServer
from impl.launcher import TestLauncher


def main(the_class, the_file):
    installation_path = os.path.split(__file__)[0]
    config = FileConfiguration(os.path.join(installation_path, "config.ini"))
    lib_path = os.path.join(installation_path, "lib")

    java_filename = JavaClassGenerator().run([the_file])[0]

    java_directory = os.path.split(the_file)[0]
    classpath = Classpath(lib_path)
    classpath.addDirectory(java_directory)

    executor = CommandExecutor()
    java_class_filename = JavaFileCompiler(config, classpath, executor).compile([java_filename])[0]
    
    xmlRpcServer = XmlRpcServer(config)
    java_launcher = JavaTestLauncher(config, classpath, executor)
    TestLauncher(xmlRpcServer, java_launcher).launch([(the_file, java_class_filename)])
    
    os.remove(java_filename)
    os.remove(java_filename.replace('.java', '.class'))
