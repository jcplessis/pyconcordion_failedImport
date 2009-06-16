from concordion.impl.annotation import ExpectedToFail, ExpectedToPass, Unimplemented
import unittest
import os



class AnnotationsTest(unittest.TestCase):
    
    def testUnimplemented(self):
        "Annotation - @Unimplemented exists and sets __pyconcordion_expected"
        @Unimplemented
        class the_class:
            pass
        self.assertEquals('Unimplemented', the_class._pyconcordion_expected)
        
    def testExpectesToFail(self):
        "Annotation - @ExpectedToFail exists and sets __pyconcordion_expected"
        @ExpectedToFail
        class the_class:
            pass
        self.assertEquals('ExpectedToFail', the_class._pyconcordion_expected)
    
    def testExpectedToPass(self):
        "Annotation - @ExpectedToPass exists and sets __pyconcordion_expected"
        @ExpectedToPass
        class the_class:
            pass
        self.assertEquals('ExpectedToPass', the_class._pyconcordion_expected)
