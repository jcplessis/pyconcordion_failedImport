import os

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
    
    def __init__(self, config=None):
        if not config:
            config = {'port':1337}
        self.config = config
    
    def run(self, python_files):
        result = []
        for python_file in python_files:
            java_file = python_file.replace(".py", ".java")
            python_module = {}
            execfile(python_file, python_module)
            python_class = os.path.split(python_file)[1].replace(".py", "");
            python_instance = python_module[python_class]()
            java_content = self.generate(python_instance)
            file(java_file, "w").write(java_content)
            result.append(python_file.replace(".py", ".java"))
        return result
    
    def generate(self, python_instance):
        return "".join([imports, 
                        class_declaration%{"name":python_instance.__class__.__name__}, 
                        attributes, 
                        setup%self.config['port'],
                        "\n".join(self.generateMethods(python_instance)), 
                        footer])
        
    def generateMethods(self, python_instance):
        methods = []
        for method_name in dir(python_instance):
            if not method_name.startswith("_"):
                method = getattr(python_instance, method_name)
                arguments = method.func_code.co_varnames
                arguments_list=", ".join(arguments[1:])
                arguments_declaration=", ".join(["String " + x for x in arguments[1:]])
                methods.append(method_template%{"name":method_name, "args_declaration":arguments_declaration, "args_list":arguments_list})
        return methods