import os, threading, sys
from SimpleXMLRPCServer import SimpleXMLRPCServer

class XmlRpcServer:
    def __init__(self, configuration, files):
        self.configuration = configuration
        self.files = files

    def launch(self):
        self.server = XMLRPCServerThread(int(self.configuration.get("server_port")))
        for file in self.files:
            module_name = os.path.basename(file).replace(".pyc", "").replace(".py", "")
            dir = os.path.dirname(file)
            sys.path.append(dir)
            exec "import " + module_name
            exec "instance=" + module_name + "." + module_name + "()"
            self.server.add_instance(instance)

        self.thread = threading.Thread(target=self.server)
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        try:
            self.server.stop()
            self.thread.join()
        except Exception, e:
            pass # In python 2.5 we can't stop the xmlrpc server


class XMLRPCServerThread:
    def __init__(self, port):
        self.server = SimpleXMLRPCServer(("localhost", port), logRequests=False, allow_none=True)

    def add_instance(self, instance):
        for key in dir(instance):
            attr = getattr(instance, key)
            if isinstance(attr, self.__init__.__class__):
                self.server.register_function(attr, instance.__class__.__name__ + "_" + getattr(attr, "_real_name", attr.__name__))

    def __call__(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
