import unittest
import pmock
import xmlrpclib
from concordion.impl.xmlrpc import XmlRpcServer

class XmlRpcServerTest(unittest.TestCase):
    
    def testCanLaunchAndStopAServer(self):
        "XmlRpcServer - can be launched and stopped"
        config = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("server_port")).will(pmock.return_value("8000"))
        server = XmlRpcServer(__file__, config)
        self.assertNotAvailable()
        server.launch()
        self.assertAvailable()
        server.stop()
        self.assertNotAvailable()
        
    def assertNotAvailable(self):
        server = xmlrpclib.ServerProxy("http://localhost:8000")
        try:
            server.echo("polop")
            self.fail("Should have thrown exception")
        except Exception, (code, message):
            self.assertEquals('Connection refused', message)
       
    def assertAvailable(self): 
        server = xmlrpclib.ServerProxy("http://localhost:8000")
        try:
            server.echo("polop")
        except Exception, value:
            self.fail("Shouldn't have thrown exception : " + repr(value))

class xmlrpc_test:
    def echo(self, s):
        return s