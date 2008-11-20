from concordion import concordion

class PythonTest:
	
	def getMessage(self):
		return "Concordion supports python"
	
if __name__ == '__main__':
	concordion.main(PythonTest, __file__)
