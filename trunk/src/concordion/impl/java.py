import os
import glob

package = """
package %s
"""

imports="""
import java.net.*;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;
import java.lang.reflect.Array;
import java.util.*;
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
public Object %(name)s(%(args_declaration)s) throws XmlRpcException{
    Object result = this.client.execute("%(name)s", new Object[]{%(args_list)s});
    if(result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}"""


class JavaClassGenerator:
    
    def __init__(self, configuration=None):
        if not configuration:
            configuration = {'port':1337}
        self.configuration = configuration
    
    def run(self, python_files):
        result = []
        for python_file in python_files:
            java_file = python_file.replace(".py", ".java")
            python_module = {}
            execfile(python_file, python_module)
            python_class_name = os.path.split(python_file)[1].replace(".py", "");
            python_class = python_module[python_class_name]
            java_content = self.generate(python_class)
            file(java_file, "w").write(java_content)
            result.append(python_file.replace(".py", ".java"))
        return result
    
    def generate(self, python_class):
        return "".join([imports, 
                        class_declaration%{"name":python_class.__name__}, 
                        attributes, 
                        setup%self.configuration['port'],
                        "\n".join(self.generateMethods(python_class)), 
                        footer])
        
    def generateMethods(self, python_class):
        methods = []
        for method_name in dir(python_class):
            if not method_name.startswith("_"):
                method = getattr(python_class, method_name)
                arguments = method.func_code.co_varnames[:method.func_code.co_argcount]
                arguments_list=", ".join(arguments[1:])
                arguments_declaration=", ".join(["String " + x for x in arguments[1:]])
                methods.append(method_template%{"name":method_name, "args_declaration":arguments_declaration, "args_list":arguments_list})
        return methods
    
class Classpath:
    def __init__(self, path):
        self.path = path
        self.directories = []
    
    def getClasspath(self):
        files = glob.glob(os.path.join(self.path, "*.jar"))
        absolute_files = map(os.path.abspath, files)
        absolute_files.extend(self.directories)
        return '"' + os.pathsep.join(absolute_files) + '"'
    
    def addDirectory(self, path):
        self.directories.append(path)
        
    def removeDirectory(self, path):
        self.directories.remove(path)
    
    def addDirectories(self, paths):
        for path in paths:
            self.addDirectory(path)
        
class JavaFileCompiler:
    def __init__(self, config, classpath, executor):
        self.configuration = config
        self.classpath = classpath
        self.executor = executor
        
    def compile(self, javaFiles):
        command = " ".join([self.configuration.get("javac_command"), "-cp", self.classpath.getClasspath(), " ".join(javaFiles)])
        if self.executor.run(command) != 0:
            raise Exception("Sorry, an exception occured in the compilation process")
        def modifyExtension(file):
            name, extension = os.path.splitext(file)
            return name + ".class"
            
        return map(modifyExtension, javaFiles)
        
class JavaTestLauncher:
    def __init__(self, config, classpath, executor):
        self.configuration = config
        self.classpath = classpath
        self.executor = executor
        
    def launch(self, classFile):
        className = os.path.basename(classFile).replace(".class", "")
        directory = os.path.split(classFile)[0]
        self.classpath.addDirectory(directory)
        command = " ".join([self.configuration.get('java_command'),
                "-Dconcordion.output.dir="+ os.path.join(self.configuration.get('output_folder'), directory),
                "-cp",
                self.classpath.getClasspath(),
                "junit.textui.TestRunner",
                className])
        execution_result = self.executor.run(command, True)
        self.classpath.removeDirectory(directory)
        if execution_result != 0:
            raise Exception("Sorry, an exception occured in the test launching process")