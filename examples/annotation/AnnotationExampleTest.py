from concordion.annotation import ExpectedToFail

@ExpectedToFail
class AnnotationExampleTest:
	
	def isFalse(self):
		return False
	
