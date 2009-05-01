import os, threading
from SimpleXMLRPCServer import SimpleXMLRPCServer

class XmlRpcServer:
    def __init__(self, configuration):
        self.configuration = configuration
    
    def launch(self, file):
        module_name = os.path.basename(file).replace(".pyc", "").replace(".py", "")
        exec "import " + module_name
        exec "instance=" + module_name + "." + module_name + "()"
        self.server = XMLRPCServerThread(instance, int(self.configuration.get("server_port")))
        self.thread = threading.Thread(target=self.server)
        self.thread.setDaemon(True)
        self.thread.start()
    
    def stop(self):
        self.server.stop()
        self.thread.join()


class XMLRPCServerThread:
    def __init__(self, instance, port):
        self.server = SimpleXMLRPCServer(("localhost", port), logRequests=False, allow_none=True)
        self.server.register_instance(instance)
        
    def __call__(self):
        self.server.serve_forever()
        
    def stop(self):
        self.server.shutdown()
        self.server.server_close()