import re

class ArrayExampleTest:
	
	def __init__(self):
		self.users = []
	
	def addUser(self, user):
		self.users.append(user)
		return "ok"
	
	def getUsersContaining(self, text):
		res = []
		matcher = re.compile(text)
		for user in self.users:
			if matcher.findall(user):
				res.append(user)
		return res
	
