
imports="""
import java.net.*;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;
"""
class_declaration="""
public class %(name)s extends ConcordionTestCase{
"""
attributes="""
    XmlRpcClient client = null;
"""
setup="""
    public void setUp() throws MalformedURLException{
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://localhost:%s/"));
        this.client = new XmlRpcClient();
        this.client.setConfig(config);
    }"""

footer="""
}"""

method_template = """
public String %(name)s(%(args_declaration)s) throws XmlRpcException{
    return (String) this.client.execute("%(name)s", new Object[]{%(args_list)s});
}"""


class JavaClassGenerator:
    def __init__(self, python_instance, port):
        self.python_instance=python_instance
        self.port = port
    
    def generate(self):
        return "".join([imports, 
                        class_declaration%{"name":self.python_instance.__class__.__name__}, 
                        attributes, 
                        setup%self.port,
                        "\n".join(self.generateMethods()), 
                        footer])
        
    def generateMethods(self):
        methods = []
        for method_name in dir(self.python_instance):
            if not method_name.startswith("_"):
                method = getattr(self.python_instance, method_name)
                arguments = method.func_code.co_varnames
                arguments_list=", ".join(arguments[1:])
                arguments_declaration=", ".join(["String " + x for x in arguments[1:]])
                methods.append(method_template%{"name":method_name, "args_declaration":arguments_declaration, "args_list":arguments_list})
        return methods