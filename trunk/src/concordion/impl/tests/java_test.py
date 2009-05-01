import unittest, os, shutil, pmock

from concordion.impl.java import JavaClassGenerator, Classpath, JavaFileCompiler, JavaTestLauncher

class JavaClassGeneratorTest(unittest.TestCase):
    
    def test_can_generate_for_an_empty_list_of_classes(self):
        "Class Generator - Can be run on an empty file list"
        generator = JavaClassGenerator()
        self.assertEquals([], generator.run([]))
        
    def test_can_generate_for_a_single_simple_python_file(self):
        "Class Generator - Can be run on a single simple python file"
        _createFile("MyPythonFile.py", """
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator().run(["MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("MyPythonFile.java", result[0])
        self.assertEquals("""
import java.net.*;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.XmlRpcException;
import org.concordion.integration.junit3.ConcordionTestCase;
import java.lang.reflect.Array;
import java.util.*;

public class MyPythonFile extends ConcordionTestCase{

    XmlRpcClient client = null;

    public void setUp() throws MalformedURLException{
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://localhost:1337/"));
        this.client = new XmlRpcClient();
        this.client.setConfig(config);
    }
}""", file(result[0]).read())
        os.remove("MyPythonFile.py")
        os.remove("MyPythonFile.java")
        
    def test_can_generate_java_method_for_an_argument_less_python_method(self):
        "Class Generator - Can generate Java method for an argument less python method"
        _createFile("MyPythonFile2.py", """
class MyPythonFile2:
    def do_plop(self):
        pass
""")
        JavaClassGenerator().run(["MyPythonFile2.py"])
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public Object do_plop() throws XmlRpcException{
    Object result = this.client.execute("do_plop", new Object[]{});
    if(result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}""")>=0)
        os.remove("MyPythonFile2.py")
        os.remove("MyPythonFile2.java")
    
    # This test is a bug fix !    
    def test_can_generate_correct_java_even_if_method_contains_variables(self):
        "Class Generator - Can generate Java method even if python contains local variables"
        
        _createFile("MyPythonFile2.py", """
class MyPythonFile2:
    def do_plop(self):
        local_variable = "polop"
""")
        JavaClassGenerator().run(["MyPythonFile2.py"])
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public Object do_plop() throws XmlRpcException{
    Object result = this.client.execute("do_plop", new Object[]{});
    if(result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}""")>=0)
        os.remove("MyPythonFile2.py")
        os.remove("MyPythonFile2.java")

    def test_can_generate_java_method_for_a_python_method_with_arguments(self):
        "Class Generator - Can generate Java method for a python method with arguments"
        _createFile("MyPythonFile3.py", """
class MyPythonFile3:
    def do_plop(self, polop, pilip):
        pass
""")
        JavaClassGenerator().run(["MyPythonFile3.py"])
        self.assertTrue(file("MyPythonFile3.java").read().find("""
public Object do_plop(String polop, String pilip) throws XmlRpcException{
    Object result = this.client.execute("do_plop", new Object[]{polop, pilip});
    if(result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}""")>=0)
        os.remove("MyPythonFile3.py")
        os.remove("MyPythonFile3.java")
        
        
    def test_can_generate_for_a_simple_python_file_in_another_directory(self):
        "Class Generator - Can generate even for a file that is not in the same directory"
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        _createFile("tmp/MyPythonFile.py", """
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator().run(["tmp/MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("tmp/MyPythonFile.java", result[0])
        shutil.rmtree("tmp")
        
    
        
        
class ClasspathTest(unittest.TestCase):
    
    def setUp(self):
        if not os.path.exists("lib"):
            os.mkdir("lib")
            
    def tearDown(self):
        shutil.rmtree("lib");
    
    def testEmptyClassPath(self):
        "Classpath - can create empty classpath"
        self.assertEquals("", Classpath("lib").getClasspath())
        
    def testCanAddADirectoryToAnEmptyClasspath(self):
        "Classpath - can add a directory to empty classpath"
        classpath = Classpath("lib")
        classpath.addDirectory("/tmp")
        self.assertEquals("/tmp", classpath.getClasspath())
        
    def testCanRemoveADirectory(self):
        "Classpath - can remove a directory"
        classpath = Classpath("lib")
        classpath.addDirectory("/tmp")
        classpath.removeDirectory("/tmp")
        self.assertEquals("", classpath.getClasspath())
        
        
    def testClasspathWithOneJar(self):
        "Classpath - can create classpath with one jar"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        self.assertEquals(path, Classpath("lib").getClasspath())
        
    def testClasspathWithManyJar(self):
        "Classpath - can create classpath with many jars"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        path2 = _createFile(os.path.join("lib", "test2.jar"), "polop aussi")
        self.assertEquals(path + ":" + path2, Classpath("lib").getClasspath())
        
    def testClasspathWithManyDirectoriesAdded(self):
        "Classpath - can add many directories to a classpath"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        path2 = _createFile(os.path.join("lib", "test2.jar"), "polop aussi")
        classpath = Classpath("lib")
        classpath.addDirectories(["lib", "/tmp"])
        self.assertEquals(path + ":" + path2 + ":lib:/tmp", classpath.getClasspath())

class JavaFileCompilerTest(unittest.TestCase):
    def testCanCompile(self):
        "JavaFileCompiler - can compile files"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("javac_command")).will(pmock.return_value("myJavac"))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath"))
        executor.expects(pmock.once()).run(pmock.eq("myJavac -cp myclasspath polop/MyClass.java a/pif.java")).will(pmock.return_value(0))
        result = JavaFileCompiler(config, classpath, executor).compile(["polop/MyClass.java", "a/pif.java"])
        self.assertEquals(["polop/MyClass.class", "a/pif.class"], result)
        
    def testRaisesExceptionInCaseCompilationFails(self):
        "JavaFileCompiler - raises exception in case compilation fails"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).method("get").will(pmock.return_value(""))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath"))
        executor.expects(pmock.once()).method("run").will(pmock.return_value(1))
        try:
            result = JavaFileCompiler(config, classpath, executor).compile(["polop/MyClass.java"])
            self.fail("Should have raised an exception")
        except Exception, e:
            self.assertEquals("Sorry, an exception occured in the compilation process", str(e)  )
        
class JavaTestLauncherTest(unittest.TestCase):
    def testCanLaunchAndReturnOK(self):
        "JavaTestLauncher - can launch a file and returns OK if executor returns OK"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value("myJava"))
        config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("myOutput"))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath"))
        classpath.expects(pmock.once()).addDirectory(pmock.eq("polop"))
        classpath.expects(pmock.once()).removeDirectory(pmock.eq("polop"))
        executor.expects(pmock.once()).run(pmock.eq("myJava -Dconcordion.output.dir=myOutput -cp myclasspath junit.textui.TestRunner MyClass"), pmock.eq(True)).will(pmock.return_value(0))
        
        JavaTestLauncher(config, classpath, executor).launch("polop/MyClass.class")
        
    def testAddsAndRemovesDirectoriesFromClasspath(self):
        "JavaTestLauncher - when launching a file it adds the directory to the classpath and removes it after"
        mock = pmock.Mock()
        mock.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value("myJava"))
        mock.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("myOutput"))
        
        mock.expects(pmock.once()).addDirectory(pmock.eq("polop")).id("add")
        mock.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath;polop")).after("add").id("getPath")
        mock.expects(pmock.once()).run(pmock.eq("myJava -Dconcordion.output.dir=myOutput -cp myclasspath;polop junit.textui.TestRunner MyClass"), pmock.eq(True)) \
            .will(pmock.return_value(0)).id("exec").after("getPath")
        mock.expects(pmock.once()).removeDirectory(pmock.eq("polop")).after("exec")
        
        JavaTestLauncher(mock, mock, mock).launch("polop/MyClass.class")
        
    def testCanLaunchAndRaiseWhenFailureOccurs(self):
        "JavaTestLauncher - can launch a file and raise an exception when compile fails"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value(""))
        config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value(""))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value(""))
        classpath.expects(pmock.once()).addDirectory(pmock.eq(""))
        classpath.expects(pmock.once()).removeDirectory(pmock.eq(""))

        executor.expects(pmock.once()).method("run").will(pmock.return_value(1))
        try:
            result = JavaTestLauncher(config, classpath, executor).launch("")
            self.fail("Should have raised an exception")
        except Exception, e:
            self.assertEquals("Sorry, an exception occured in the test launching process", str(e))
        
        
        
def _createFile(name, content):
        file(name, "w").write(content)
        return os.path.abspath(name);