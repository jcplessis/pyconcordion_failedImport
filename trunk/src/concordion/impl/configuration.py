
class FileConfiguration:
    def __init__(self, filename):
        self.filename = filename
        self.properties = None
        
    def _init(self):
        if not self.properties:
            self.properties = {}
            execfile(self.filename, self.properties)
            del self.properties['__builtins__']
    
    def keys(self):
        self._init()
        return self.properties.keys()
    
    def get(self, keyname):
        return self.properties[keyname]
    