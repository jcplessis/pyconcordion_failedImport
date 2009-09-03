import os
import glob

package = """
package %s;
"""

imports="""
import java.net.*;
import org.apache.ws.commons.util.NamespaceContextImpl;
import org.apache.xmlrpc.common.TypeFactoryImpl;
import org.apache.xmlrpc.common.XmlRpcController;
import org.apache.xmlrpc.common.XmlRpcStreamConfig;
import org.apache.xmlrpc.parser.NullParser;
import org.apache.xmlrpc.parser.TypeParser;
import org.apache.xmlrpc.serializer.NullSerializer;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;
import org.concordion.api.%(expected)s;
import java.lang.reflect.Array;
import java.util.*;
"""
class_declaration="""
@%(expected)s
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
        this.client.setTypeFactory(new MyTypeFactory(this.client));
        this.client.setConfig(config);
    }"""

footer="""

    class MyTypeFactory extends TypeFactoryImpl {
    
        public MyTypeFactory(XmlRpcController pController) {
            super(pController);
        }
    
        @Override
        public TypeParser getParser(XmlRpcStreamConfig pConfig,
          NamespaceContextImpl pContext, String pURI, String pLocalName) {
    
            if ("".equals(pURI) && NullSerializer.NIL_TAG.equals(pLocalName)) {
                return new NullParser();
            } else {
                return super.getParser(pConfig, pContext, pURI, pLocalName);
            }
        }
    }
}"""

method_template = """
public Object %(name)s(%(args_declaration)s) throws XmlRpcException{
    Object result = this.client.execute("%(class_name)s_%(name)s", new Object[]{%(args_list)s});
    if(result != null && result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}"""

suite_template = """import junit.framework.Test;
import junit.framework.TestSuite;


public class Suite {
    public static Test suite(){
        TestSuite suite = new TestSuite();
        suite.setName("pyConcordion test suite");
%(tests)s
        return suite;
    }
}
"""

add_test_template = '        suite.addTest(new TestSuite(%(class_full_path)s.class));'
        
class JavaClassGenerator:
    
    def __init__(self, root_dir, configuration=None):
        if not configuration:
            configuration = {'server_port':1337}
        self.configuration = configuration
        self.root_dir = root_dir
    
    def run(self, python_files):
        result = []
        for python_file in python_files:
            java_file = python_file.replace(".py", ".java")
            python_module = {}
            execfile(python_file, python_module)
            python_class_name = os.path.split(python_file)[1].replace(".py", "");
            python_class = python_module[python_class_name]
            java_content = self.generate(python_class, python_file)
            file(java_file, "w").write(java_content)
            result.append(python_file.replace(".py", ".java"))
        return result
    
    def suite(self, java_files):
        add_tests = []
        for file in java_files:
            file_from_root = os.path.abspath(file)[len(os.path.abspath(self.root_dir))+1:]
            full_path = file_from_root.replace('.java', '').replace(os.sep, '.')
            add_tests.append(add_test_template%{"class_full_path":full_path})
        suite_file = os.path.join(self.root_dir, "Suite.java")
        open(suite_file, "w").write(suite_template%{"tests" : "\n".join(add_tests)})
        return suite_file
    
    def generate(self, python_class, python_file):
        expected = "ExpectedToPass"
        try:
            expected = python_class._pyconcordion_expected
        except AttributeError:
            pass
        return "".join([self.generate_package(python_file),
                        imports%{"expected" : expected}, 
                        class_declaration%{"name":python_class.__name__, "expected" : expected}, 
                        attributes, 
                        setup%self.configuration.get('server_port'),
                        "\n".join(self.generateMethods(python_class)), 
                        footer])
    
    def generate_package(self, python_file):
        file_from_root = os.path.abspath(python_file)[len(os.path.abspath(self.root_dir))+1:]
        file_package = os.path.split(file_from_root)[0]
        if file_package == "":
            return ""
        else:
            return package%file_package.replace(os.sep, ".")
    
    def generateMethods(self, python_class):
        methods = []
        for method_name in dir(python_class):
            if not method_name.startswith("_"):
                method = getattr(python_class, method_name)
                if isinstance(method, type(self.generateMethods)):
                    arguments = method.func_code.co_varnames[:method.func_code.co_argcount]
                    arguments_list=", ".join(arguments[1:])
                    arguments_declaration=", ".join(["String " + x for x in arguments[1:]])
                    methods.append(method_template%{"name":method_name, "class_name":python_class.__name__, "args_declaration":arguments_declaration, "args_list":arguments_list})
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
    def __init__(self, config, classpath, executor, root_dir):
        self.configuration = config
        self.classpath = classpath
        self.executor = executor
        self.root_dir = root_dir
        
    def launch(self, classFile):
        (directory, name) = os.path.split(classFile)
        className = name.replace(".class", "")
        package = os.path.abspath(directory)[len(os.path.abspath(self.root_dir))+1:].replace(os.sep, ".")
        class_full_path = None
        if package == "":
            class_full_path = className
        else:
            class_full_path = package + "." + className

        self.classpath.addDirectory(self.root_dir)
        command = " ".join([self.configuration.get('java_command'),
                "-Dconcordion.output.dir="+ self.configuration.get('output_folder'),
                "-cp",
                self.classpath.getClasspath(),
                "junit.textui.TestRunner",
                class_full_path])
        execution_result = self.executor.run(command, True)
        self.classpath.removeDirectory(self.root_dir)
        return execution_result
