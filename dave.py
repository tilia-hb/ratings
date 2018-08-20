class Cat():
	def __init__(self, color):
		self.color = color

	@classmethod
	def gimme_a_cat(cls, color):
		return Cat(color)

	def my_instance_method(self, color):
		print("self is", self, "color is", color)