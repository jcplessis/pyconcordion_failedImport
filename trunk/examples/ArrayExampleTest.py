class ArrayExampleTest:
	
	def __init__(self):
		self.users = []
	
	def getUsers(self):
		return tuple(self.users)
	
	def addUser(self, user):
		self.users.append(user)
		return "ok"
	
