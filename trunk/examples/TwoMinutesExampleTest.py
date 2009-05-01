from concordion import concordion

class TwoMinutesExampleTest:
	
	def getMessage(self):
		return "Concordion supports python"
	
if __name__ == '__main__':
	concordion.main(__file__)
