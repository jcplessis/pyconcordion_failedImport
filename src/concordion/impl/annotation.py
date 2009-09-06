def ExpectedToFail(clazz):
    clazz._pyconcordion_expected = 'ExpectedToFail'
    return clazz

def ExpectedToPass(clazz):
    clazz._pyconcordion_expected = 'ExpectedToPass'
    return clazz

def Unimplemented(clazz):
    clazz._pyconcordion_expected = 'Unimplemented'
    return clazz

class ExpectedToFailClass:
    _pyconcordion_expected = 'ExpectedToFail'

class ExpectedToPassClass:
    _pyconcordion_expected = 'ExpectedToPass'
    
class UnimplementedClass:
    _pyconcordion_expected = 'Unimplemented'   
