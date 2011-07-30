from concordion import concordion_convert_parameters

class ConvertersExampleTest:

	@concordion_convert_parameters(int, int)
	def add_integers(self, a, b):
		return a + b

	@concordion_convert_parameters(float, float)
	def add_floats(self, a, b):
		return a + b

