import turtle
turtle.speed(0)
turtle.delay(0)
turtle.ht()
turtle.up()
turtle.pencolor("#D6B5B5")
BACKGROUND = "#252525"

class DragonHandler:
	def __init__(self, settings):
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.width = 500
		self.height = 500
		self.bg = BACKGROUND

		turtle.screensize(self.width, self.height, self.bg)
		turtle.degrees(360) 
		turtle.setpos(-self.width/4, 0)
		turtle.setheading(90) 


	def execute_command(self, command):
		curr_heading = turtle.heading()
		if command == "F":
			turtle.forward(self.length)
		elif command == "+":
			turtle.right(self.angle)
		elif command == "-":
			turtle.left(self.angle)

	def draw(self, strings):
		turtle.down()
		for string in strings:
			for command in string:
				self.execute_command(command)
		turtle.done()

class KochHandler:
	def __init__(self, settings):
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.width = 500
		self.height = 500
		self.bg = BACKGROUND

		turtle.screensize(self.width, self.height, self.bg) 
		turtle.degrees(360) 	
		turtle.setpos(-self.width/2, -self.height/2)


	def execute_command(self, command):
		curr_heading = turtle.heading()
		if command == "F":
			turtle.forward(self.length)
		elif command == "-":
			turtle.right(self.angle)
		elif command == "+":
			turtle.left(self.angle)

	def draw(self, strings):
		turtle.down()
		for string in strings:
			for command in string:
				self.execute_command(command)
		turtle.done()

class PlantHandler:
	def __init__(self, settings):
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.width = 500
		self.height = 500
		self.bg = BACKGROUND
		self.stack = []

		turtle.screensize(self.width, self.height, self.bg) 
		turtle.degrees(360) 	
		turtle.setheading(90)
		turtle.setpos(0, -self.height/2)


	def execute_command(self, command):
		curr_heading = turtle.heading()
		if command == "F":
			turtle.forward(self.length)
		elif command == "-":
			turtle.right(self.angle)
		elif command == "+":
			turtle.left(self.angle)
		elif command == "[":
			self.stack.append({"pos": turtle.pos(), "heading": turtle.heading()})
		elif command == "]":
			cmd = self.stack.pop()
			turtle.up()
			turtle.setheading(cmd["heading"])
			turtle.setpos(cmd["pos"])
			turtle.down()

	def draw(self, strings):
		turtle.down()
		for string in strings:
			for command in string:
				self.execute_command(command)
		turtle.done()


class BTreeHandler:
	def __init__(self, settings):
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.width = 500
		self.height = 500
		self.bg = BACKGROUND
		self.stack = []

		turtle.screensize(self.width, self.height, self.bg) 
		turtle.degrees(360) 	
		turtle.setheading(90)
		turtle.setpos(0, -self.height/2)


	def execute_command(self, command):
		curr_heading = turtle.heading()
		if command == "0" or command == "1":
			turtle.forward(self.length) 
		elif command == "[":
			self.stack.append({"pos": turtle.pos(), "heading": turtle.heading()})
			turtle.left(self.angle) 
		elif command == "]":
			cmd = self.stack.pop()
			turtle.up()
			turtle.setheading(cmd["heading"])
			turtle.setpos(cmd["pos"])
			turtle.right(self.angle)
			turtle.down()

	def draw(self, strings):
		turtle.down()
		for string in strings:
			for command in string:
				self.execute_command(command) 
		turtle.done()