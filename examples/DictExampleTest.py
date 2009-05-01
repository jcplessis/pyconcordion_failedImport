import re

class user:
	def __init__(self, name, age):
		self.name = name
		self.age = age
		
class DictExampleTest:
	
	def getUsersAsDict(self):
		return [
			{"name":"Britney", "age":30},
			{"name":"Madonna", "age":50},
		]
	
	
	def getUsersAsObj(self):
		return [
		    user("Britney", 30),
		    user("Madonna", 50),
		]
		
		
