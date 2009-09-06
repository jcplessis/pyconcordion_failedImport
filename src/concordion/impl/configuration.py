class AbstractConfiguration:
    properties = None
    
    def _init(self):
         if not self.properties:
            self.properties = {}
            self._specific_init()
    
    def _specific_init(self):
        raise Exception('Abstract')
    
    def keys(self):
        self._init()
        return self.properties.keys()
    
    def get(self, keyname):
        self._init()
        return self.properties[keyname]

class FileConfiguration(AbstractConfiguration):
    def __init__(self, filename):
        self.filename = filename
        
    def _specific_init(self):
       execfile(self.filename, self.properties)
       del self.properties['__builtins__']
    
class DictionnaryConfiguration(AbstractConfiguration):
    def __init__(self, properties):
        self.properties = properties
        
    def _specific_init(self):
        pass
    
class HierarchicalConfiguration:
    def __init__(self, configurations):
        self.configurations = configurations
    
    def get(self, keyname):
        for configuration in self.configurations:
            try:
                return configuration.get(keyname)
            except Exception, e:
                pass
        raise KeyError(keyname)
        