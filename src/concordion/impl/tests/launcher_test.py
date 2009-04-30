import unittest, pmock

from concordion.impl.launcher import TestLauncher

class LauncherGeneratorTest(unittest.TestCase):
    
    def testLaunchingEmptyList(self):
        "Launcher - Test launching empty list of tests"
        TestLauncher(None, None).launch([])


    def testLaunchingOneTest(self):
        "Launcher - Test launching one test"
        mock = pmock.Mock()
        mock.expects(pmock.once()).launch(pmock.eq("polop.py")).id("launch_xml")
        mock.expects(pmock.once()).launch(pmock.eq("polop.class")).after("launch_xml").id("launch_test")
        mock.expects(pmock.once()).stop().after("launch_test")
        TestLauncher(mock, mock).launch([("polop.py", "polop.class")])
        mock.verify()

    def testLaunchingTwoTests(self):
        "Launcher - Test launching two tests"
        mock = pmock.Mock()
        mock.expects(pmock.once()).launch(pmock.eq("polop.py")).id("launch_xml_1")
        mock.expects(pmock.once()).launch(pmock.eq("polop.class")).after("launch_xml_1").id("launch_test_1")
        mock.expects(pmock.once()).stop().after("launch_test_1").id("stop_1")
        mock.expects(pmock.once()).launch(pmock.eq("pilip.py")).after("stop_1").id("launch_xml_2")
        mock.expects(pmock.once()).launch(pmock.eq("pilip.class")).after("launch_xml_2").id("launch_test_2")
        mock.expects(pmock.once()).stop().after("launch_test_2")
        TestLauncher(mock, mock).launch([("polop.py", "polop.class"), ("pilip.py", "pilip.class")])
        mock.verify()
