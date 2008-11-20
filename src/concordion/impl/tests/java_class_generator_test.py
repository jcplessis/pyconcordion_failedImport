import unittest
from concordion.impl.java_class_generator import JavaClassGenerator

class JavaClassGeneratorTest(unittest.TestCase):
    
    def test_can_generate_empty_java_class(self):
        "Class Generator - Can generate an 'empty' java file"
        class testClass:
            pass
        java_class = JavaClassGenerator(testClass(), 8000).generate()
        self.assertEquals("""
import java.net.*;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;

public class testClass extends ConcordionTestCase{

    XmlRpcClient client = null;

    public void setUp() throws MalformedURLException{
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://localhost:8000/"));
        this.client = new XmlRpcClient();
        this.client.setConfig(config);
    }
}""", java_class)
        
        
        
    def test_can_generate_java_method_for_an_argument_less_python_method(self):
        "Class Generator - Can generate Java method for an argument less python method"
        class testClass:
            def do_plop(self):
                pass
        java_class = JavaClassGenerator(testClass(), 8000).generate()
        self.assertTrue(java_class.find("""
public String do_plop() throws XmlRpcException{
    return (String) this.client.execute("do_plop", new Object[]{});
}""")>=0)
        
    def test_can_generate_java_method_for_a_python_method_with_arguments(self):
        "Class Generator - Can generate Java method for a python method with arguments"
        class testClass:
            def do_plop(self, polop, pilip):
                pass
        java_class = JavaClassGenerator(testClass(), 8000).generate()
        self.assertTrue(java_class.find("""
public String do_plop(String polop, String pilip) throws XmlRpcException{
    return (String) this.client.execute("do_plop", new Object[]{polop, pilip});
}""")>=0, java_class)
