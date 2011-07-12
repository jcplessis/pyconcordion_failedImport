import unittest, os, shutil, pmock

from concordion.impl.java import JavaClassGenerator, Classpath, JavaFileCompiler, JavaTestLauncher

class JavaClassGeneratorTest(unittest.TestCase):

    def test_can_generate_for_an_empty_list_of_classes(self):
        "Class Generator - Can be run on an empty file list"
        generator = JavaClassGenerator(".")
        self.assertEquals([], generator.run([]))

    def test_can_generate_for_a_single_simple_python_file(self):
        "Class Generator - Can be run on a single simple python file"
        _createFile("MyPythonFile.py", """
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator(".").run(["MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("MyPythonFile.java", result[0])
        self.assertEquals("""
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
import org.concordion.api.ExpectedToPass;
import java.lang.reflect.Array;
import java.lang.System;
import java.util.*;

@ExpectedToPass
public class MyPythonFile extends ConcordionTestCase{

    XmlRpcClient client = null;

    public MyPythonFile() throws MalformedURLException{
        XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
        config.setServerURL(new URL("http://localhost:1337/"));
        this.client = new XmlRpcClient();
        this.client.setTypeFactory(new MyTypeFactory(this.client));
        this.client.setConfig(config);
        System.setProperty("concordion.extensions", "org.concordion.ext.Extensions");
    }

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
        JavaClassGenerator(".").run(["MyPythonFile2.py"])
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public Object do_plop() throws XmlRpcException{
    Object result = this.client.execute("MyPythonFile2_do_plop", new Object[]{});
    if(result != null && result.getClass().isArray()){
        List<Object> list = new ArrayList<Object>();
        for(int i = 0; i < Array.getLength(result); i++){
            list.add(Array.get(result, i));
        }
        return list;
    }
    return result;
}""") >= 0)
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
        JavaClassGenerator(".").run(["MyPythonFile2.py"])
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public Object do_plop() throws XmlRpcException{
    Object result = this.client.execute("MyPythonFile2_do_plop", new Object[]{});
""") >= 0)
        os.remove("MyPythonFile2.py")
        os.remove("MyPythonFile2.java")

    def test_can_generate_java_method_for_a_python_method_with_arguments(self):
        "Class Generator - Can generate Java method for a python method with arguments"
        _createFile("MyPythonFile3.py", """
class MyPythonFile3:
    def do_plop(self, polop, pilip):
        pass
""")
        JavaClassGenerator(".").run(["MyPythonFile3.py"])
        self.assertTrue(file("MyPythonFile3.java").read().find("""
public Object do_plop(String polop, String pilip) throws XmlRpcException{
    Object result = this.client.execute("MyPythonFile3_do_plop", new Object[]{polop, pilip});
""") >= 0)
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
        result = JavaClassGenerator("tmp/").run(["tmp/MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("tmp/MyPythonFile.java", result[0])
        shutil.rmtree("tmp")

    def test_can_generate_annotation_expected_to_fail(self):
        "Class Generator - Can generate annotation ExpectedToFail"
        _createFile("MyPythonFile.py", """
from concordion.annotation import ExpectedToFail

@ExpectedToFail
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator(".").run(["MyPythonFile.py"])

        self.assertTrue(file("MyPythonFile.java").read().find("""
@ExpectedToFail
""") >= 0)
        self.assertTrue(file("MyPythonFile.java").read().find("""
import org.concordion.api.ExpectedToFail;
""") >= 0)

    def test_can_generate_annotation_unimplemented(self):
        "Class Generator - Can generate annotation Unimplemented"
        _createFile("MyPythonFile.py", """
from concordion.annotation import Unimplemented

@Unimplemented
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator(".").run(["MyPythonFile.py"])

        self.assertTrue(file("MyPythonFile.java").read().find("""
@Unimplemented
""") >= 0)
        self.assertTrue(file("MyPythonFile.java").read().find("""
import org.concordion.api.Unimplemented;
""") >= 0)

    def test_can_generate_with_package_declaration(self):
        "Class Generator - Can generate package declaration"
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        if not os.path.exists("tmp/polop"):
            os.mkdir("tmp/polop")
        _createFile("tmp/polop/MyPythonFile.py", """
class MyPythonFile:
    pass
""")
        result = JavaClassGenerator(".").run(["tmp/polop/MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("tmp/polop/MyPythonFile.java", result[0])
        self.assertTrue(file("tmp/polop/MyPythonFile.java").read().find("""
package tmp.polop;
""") >= 0)
        shutil.rmtree("tmp")

    def test_can_generate_when_python_class_got_attributes(self):
        "Class Generator - Can generate when python class got attributes"
        _createFile("MyPythonFile.py", """
class MyPythonFile:
    attribute = []
    
    def polop(self):
        pass
""")
        result = JavaClassGenerator(".").run(["MyPythonFile.py"])
        self.assertEquals(1, len(result))
        self.assertEquals("MyPythonFile.java", result[0])
        os.remove("MyPythonFile.py")
        os.remove("MyPythonFile.java")

    def test_can_generate_java_method_for_setUp_and_tearDown(self):
        "Class Generator - Can generate for setUp and tearDown"
        _createFile("MyPythonFile2.py", """
class MyPythonFile2:
    def setUp(self):
        pass
    def tearDown(self):
        pass
""")
        JavaClassGenerator(".").run(["MyPythonFile2.py"])
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public void setUp() throws XmlRpcException{
    this.client.execute("MyPythonFile2_setUp", new Object[]{});
}""") >= 0)
        self.assertTrue(file("MyPythonFile2.java").read().find("""
public void tearDown() throws XmlRpcException{
    this.client.execute("MyPythonFile2_tearDown", new Object[]{});
}""") >= 0)
        os.remove("MyPythonFile2.py")
        os.remove("MyPythonFile2.java")

    def test_can_generate_testsuite(self):
        "Class Generator - Can generate test suite"
        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        expected = """import junit.framework.Test;
import junit.framework.TestSuite;


public class Suite {
    public static Test suite(){
        TestSuite suite = new TestSuite();
        suite.setName("pyConcordion test suite");
        suite.addTest(new TestSuite(polop.MyPythonFile.class));
        suite.addTest(new TestSuite(polop.OtherPythonFile.class));
        return suite;
    }
}
"""
        result = JavaClassGenerator("tmp").suite(["tmp/polop/MyPythonFile.java", "tmp/polop/OtherPythonFile.java"])
        self.assertEquals("tmp/Suite.java", result)
        self.assertEquals(expected, file(result).read())
        shutil.rmtree("tmp")

class ClasspathTest(unittest.TestCase):

    def setUp(self):
        if not os.path.exists("lib"):
            os.mkdir("lib")

    def tearDown(self):
        shutil.rmtree("lib");

    def testEmptyClassPath(self):
        "Classpath - can create empty classpath"
        self.assertEquals('""', Classpath("lib").getClasspath())

    def testCanAddADirectoryToAnEmptyClasspath(self):
        "Classpath - can add a directory to empty classpath"
        classpath = Classpath("lib")
        classpath.addDirectory("/tmp")
        self.assertEquals('"/tmp"', classpath.getClasspath())

    def testCanRemoveADirectory(self):
        "Classpath - can remove a directory"
        classpath = Classpath("lib")
        classpath.addDirectory("/tmp")
        classpath.removeDirectory("/tmp")
        self.assertEquals('""', classpath.getClasspath())


    def testClasspathWithOneJar(self):
        "Classpath - can create classpath with one jar"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        self.assertEquals('"' + path + '"', Classpath("lib").getClasspath())

    def testClasspathWithManyJar(self):
        "Classpath - can create classpath with many jars"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        path2 = _createFile(os.path.join("lib", "test2.jar"), "polop aussi")
        self.assertEquals('"' + path + ":" + path2 + '"', Classpath("lib").getClasspath())

    def testClasspathWithManyDirectoriesAdded(self):
        "Classpath - can add many directories to a classpath"
        path = _createFile(os.path.join("lib", "test.jar"), "polop")
        path2 = _createFile(os.path.join("lib", "test2.jar"), "polop aussi")
        classpath = Classpath("lib")
        classpath.addDirectories(["lib", "/tmp"])
        self.assertEquals('"' + path + ":" + path2 + ":lib:/tmp" + '"', classpath.getClasspath())

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
            self.assertEquals("Sorry, an exception occured in the compilation process", str(e))

class JavaTestLauncherTest(unittest.TestCase):
    def testCanLaunchAndReturnOK(self):
        "JavaTestLauncher - can launch a file and returns OK if executor returns OK"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value("myJava"))
        config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("myOutput"))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath"))
        classpath.expects(pmock.once()).addDirectory(pmock.eq("."))
        classpath.expects(pmock.once()).removeDirectory(pmock.eq("."))
        executor.expects(pmock.once()).run(pmock.eq("myJava -Dconcordion.output.dir=myOutput -cp myclasspath junit.textui.TestRunner polop.MyClass"), pmock.eq(True)).will(pmock.return_value(0))

        result = JavaTestLauncher(config, classpath, executor, ".").launch("polop/MyClass.class")
        self.assertEquals(0, result)

    def testAddsAndRemovesDirectoriesFromClasspath(self):
        "JavaTestLauncher - when launching a file it adds the directory to the classpath and removes it after"
        mock = pmock.Mock()
        mock.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value("myJava"))
        mock.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value("myOutput"))

        mock.expects(pmock.once()).addDirectory(pmock.eq(".")).id("add")
        mock.expects(pmock.once()).getClasspath().will(pmock.return_value("myclasspath;.")).after("add").id("getPath")
        mock.expects(pmock.once()).run(pmock.eq("myJava -Dconcordion.output.dir=myOutput -cp myclasspath;. junit.textui.TestRunner polop.MyClass"), pmock.eq(True)) \
            .will(pmock.return_value(0)).id("exec").after("getPath")
        mock.expects(pmock.once()).removeDirectory(pmock.eq(".")).after("exec")

        JavaTestLauncher(mock, mock, mock, ".").launch("polop/MyClass.class")

    def testCanLaunchAndReturnFailure(self):
        "JavaTestLauncher - can launch a file and return a non zero code in case of failure"
        executor = pmock.Mock()
        config = pmock.Mock()
        classpath = pmock.Mock()
        config.expects(pmock.once()).get(pmock.eq("java_command")).will(pmock.return_value(""))
        config.expects(pmock.once()).get(pmock.eq("output_folder")).will(pmock.return_value(""))
        classpath.expects(pmock.once()).getClasspath().will(pmock.return_value(""))
        classpath.expects(pmock.once()).addDirectory(pmock.eq(""))
        classpath.expects(pmock.once()).removeDirectory(pmock.eq(""))
        executor.expects(pmock.once()).method("run").will(pmock.return_value(1))
        result = JavaTestLauncher(config, classpath, executor, "").launch("")
        self.assertEquals(1, result)




def _createFile(name, content):
        file(name, "w").write(content)
        return os.path.abspath(name);
