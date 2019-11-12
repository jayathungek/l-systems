from .pen import Pen


class DragonHandler:
	def __init__(self, settings):
		self.name = "dragon"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (self.size[0]/2, self.size[0]/4)
		self.pen = Pen(self.size, self.startpos)


	def execute_command(self, command):
		curr_heading = 	self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.length)
		elif command == "+":
			self.pen.right(self.angle)
		elif command == "-":
			self.pen.left(self.angle)

	def create_image(self, strings, directory):
		self.pen.down()
		for string in strings:
			for command in string:
				self.execute_command(command)
		self.pen.show()
		self.pen.save(directory + self.name)

class KochHandler:
	def __init__(self, settings):
		self.name = "koch"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (0, self.size[1])
		self.pen = Pen(self.size, self.startpos)
 


	def execute_command(self, command):
		curr_heading = self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.length)
		elif command == "-":
			self.pen.right(self.angle)
		elif command == "+":
			self.pen.left(self.angle)

	def create_image(self, strings, directory):
		self.pen.down()
		for string in strings:
			for command in string:
				self.execute_command(command)
		self.pen.show()
		self.pen.save(directory + self.name)
		

class PlantHandler:
	def __init__(self, settings):
		self.name = "plant"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (self.size[0]/2, self.size[1])
		self.pen = Pen(self.size, self.startpos) 
		self.pen.set_heading(-90)
		self.stack = []
 


	def execute_command(self, command):
		curr_heading = self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.length)
		elif command == "-":
			self.pen.right(self.angle)
		elif command == "+":
			self.pen.left(self.angle)
		elif command == "[":
			self.stack.append({"pos": self.pen.get_pos(), "heading": self.pen.get_heading()})
		elif command == "]":
			cmd = self.stack.pop()
			self.pen.up()
			self.pen.set_heading(cmd["heading"])
			self.pen.set_pos(cmd["pos"])
			self.pen.down()

	def create_image(self, strings, directory):
		self.pen.down()
		for string in strings:
			for command in string:
				self.execute_command(command)

		self.pen.show()
		self.pen.save(directory + self.name)
		


class BTreeHandler:
	def __init__(self, settings):
		self.name = "btree"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (self.size[0]/2, self.size[1]+100)
		self.pen = Pen(self.size, self.startpos)
		self.pen.set_heading(-90)
		self.stack = []
 

	def execute_command(self, command):
		curr_heading = self.pen.get_heading()
		if command == "0" or command == "1":
			self.pen.forward(self.length) 
		elif command == "[":
			self.stack.append({"pos": self.pen.get_pos(), "heading": self.pen.get_heading()})
			self.pen.left(self.angle) 
		elif command == "]":
			cmd = self.stack.pop()
			self.pen.up()
			self.pen.set_heading(cmd["heading"])
			self.pen.set_pos(cmd["pos"])
			self.pen.right(self.angle)
			self.pen.down()

	def create_image(self, strings, directory):
		self.pen.down()
		for string in strings:
			for command in string:
				self.execute_command(command) 
		self.pen.show()
		self.pen.save(directory + self.name)
		