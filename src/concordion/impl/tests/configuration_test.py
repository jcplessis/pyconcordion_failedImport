from concordion.impl.configuration import FileConfiguration, DictionnaryConfiguration, HierarchicalConfiguration
import unittest, pmock
import os, sys

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

class DictionnaryConfigurationTest(unittest.TestCase):
    
    def _getConfig(self, properties):
        return DictionnaryConfiguration(properties)
    
    def test_can_take_empty_properties(self):
        "Dictionnary Configuration - Can be empty"
        configuration = self._getConfig({})
        self.assertEquals(0, len(configuration.keys()))
        
    def test_can_take_dictionnary(self):
        "Dictionnary Configuration - Can take a dictionnary with one entry"
        configuration = self._getConfig({"output_folder":"/tmp/polop"})
        self.assertEquals(1, len(configuration.keys()))
        self.assertEquals("/tmp/polop", configuration.get("output_folder"))

class HierarchicalConfigurationTest(unittest.TestCase):
    
    def test_cant_take_one_configuration(self):
        "Hierarchical Configuration - Can take one child configuration"
        fake_config = pmock.Mock()
        fake_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("polop"))
        configuration = HierarchicalConfiguration([fake_config])
        self.assertEquals("polop", configuration.get("output_folder"))
    
    def test_cant_take_two_configuration_first_is_default(self):
        "Hierarchical Configuration - Can take two childs configuration, first child value is returned if exist"
        fake_config = pmock.Mock()
        fake_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("polop"))
        other_config = pmock.Mock()
        configuration = HierarchicalConfiguration([fake_config, other_config])
        self.assertEquals("polop", configuration.get("output_folder"))
        
    def test_cant_take_two_configuration_second_is_called_if_necessary(self):
        "Hierarchical Configuration - Can take two childs configuration, second child is called if necessary"
        fake_config = pmock.Mock()
        fake_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.raise_exception(Exception("Uknown key...")))
        other_config = pmock.Mock()
        other_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("polop"))
        configuration = HierarchicalConfiguration([fake_config, other_config])
        self.assertEquals("polop", configuration.get("output_folder"))                                                                      
        
    def test_raises_an_exception_if_not_found(self):
        "Hierarchical Configuration - Raises an exception if not found"
        fake_config = pmock.Mock()
        fake_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.raise_exception(Exception("Uknown key...")))
        other_config = pmock.Mock()
        other_config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.raise_exception(Exception("Uknown key...")))
        configuration = HierarchicalConfiguration([fake_config, other_config])
        try:
            configuration.get("output_folder")
            self.fail("Should have thrown exception")
        except KeyError, e:
            self.assertEquals("'output_folder'", str(e))
        
