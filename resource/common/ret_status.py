class RetStatus:
	def __init__(self, status=False, msg="", data=None):
		self.status = status
		self.msg    = msg
		self.data   = data
	def check(self):
		return self.status
	def restore(self, status, msg="", data=None):
		self.status = status
		self.msg    = msg
		self.data   = data
	def dumps_json(self):
		if self.data is None:
			return {"status" : self.status, "msg" : self.msg}
		else:
			return {"status" : self.status, "msg" : self.msg, "data" : self.data}
