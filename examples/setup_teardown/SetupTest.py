class SetupTest:
	
	def setUp(self):
		self.value = True
	
	def getSetupValue(self):
		return self.value
	
	def tearDown(self):
		self.value = False