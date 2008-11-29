from concordion.impl.configuration import FileConfiguration
import unittest
import os

class FileConfigurationTest(unittest.TestCase):
    
    def setUp(self):
        self.file = file("tmp_config.ini", "w")
        self.file.write("")
        
    def tearDown(self):
        os.remove(self.file.name)
    
    def _getConfig(self):
        return FileConfiguration(self.file.name)
    
    def test_creation_with_empty_file(self):
        "File Configuration - Can read an empty file"
        configuration = self._getConfig()
        self.assertEquals(0, len(configuration.keys()))
        
    def test_reading_properties(self):
        "File Configuration - Can read a non empty file"
        self.file.write("polop=1337")
        self.file.flush()
        configuration = self._getConfig()
        self.assertEquals(1, len(configuration.keys()))
        self.assertTrue("polop" in configuration.keys())
        self.assertEquals(1337, configuration.get("polop"))
        
    def test_reading_properties_BUG(self):
        "File Configuration - BUG FIXING TEST - When using 'get' before using 'keys'"
        self.file.write("polop=1337")
        self.file.flush()
        configuration = self._getConfig()
        self.assertEquals(1337, configuration.get("polop"))
