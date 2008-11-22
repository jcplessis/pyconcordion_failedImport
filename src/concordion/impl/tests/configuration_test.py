from concordion.impl.configuration import FileConfiguration
import unittest
import os

class FileConfigurationTest(unittest.TestCase):
    
    def test_creation_with_empty_file(self):
        "File Configuration - Can read an empty file"
        file("tmp_config.ini", "w").write("")
        configuration = FileConfiguration("tmp_config.ini")
        self.assertEquals(0, len(configuration.keys()))
        os.remove("tmp_config.ini")
        
    def test_reading_properties(self):
        "File Configuration - Can read a non empty file"
        file("tmp_config.ini", "w").write("polop=1337")
        configuration = FileConfiguration("tmp_config.ini")
        self.assertEquals(1, len(configuration.keys()))
        self.assertTrue("polop" in configuration.keys())
        self.assertEquals(1337, configuration.get("polop"))
        os.remove("tmp_config.ini")