from concordion import concordion

class TwoMinutesExampleTest:
	
	def getMessage(self):
		return "Concordion supports python"
	
if __name__ == '__main__':
	concordion.main(TwoMinutesExampleTest, __file__)
