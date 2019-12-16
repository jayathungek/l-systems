from .pen import Pen
import imageio
from pygifsicle import optimize
import numpy as np
import os

IMG_EXT = ".png"
GIF_EXT = ".gif"

class Util:

	@staticmethod
	def add_value_to_hex(hex_string, value, upper_limit, lower_limit):
		value_range = upper_limit - lower_limit
		result  = int(hex_string, 16) + value
		if value_range > 0:
			if result < lower_limit:
				abs_diff = lower_limit - result
				offset = abs_diff%value_range
				result = upper_limit - offset
			if result > upper_limit:
				abs_diff = result - upper_limit
				offset = abs_diff%value_range
				result = lower_limit + offset
			padded = str.format('{:02X}', result)
			return padded 
		elif value_range == 0:
			return str.format('{:02X}', int(hex_string, 16))
		else:
			raise ValueError("Upper limit must be greater than lower limit")

	@staticmethod
	def edit_rbg_value(colour, rgb, amount, start_colour, end_colour):
		new_colour = ""
		if rgb == 'r':
			component = colour[1:3]
			upper_limit = int(start_colour[1:3], 16)
			lower_limit = int(end_colour[1:3], 16)
			component = Util.add_value_to_hex(component, amount, upper_limit, lower_limit)
			new_colour = component+colour[3:]
		elif rgb == 'g':
			component = colour[3:5]
			upper_limit = int(start_colour[3:5], 16)
			lower_limit = int(end_colour[3:5], 16)
			component = Util.add_value_to_hex(component, amount, upper_limit, lower_limit)
			new_colour = colour[1:3] + component + colour[5:]
		elif rgb == 'b':
			component = colour[5:]
			upper_limit = int(start_colour[5:], 16)
			lower_limit = int(end_colour[5:], 16)
			component = Util.add_value_to_hex(component, amount, upper_limit, lower_limit)
			new_colour =colour[1:5] + component

		return "#"+new_colour

class GifMaker:
	def __init__(self, timestep=0.5):
		self.images = []
		self.timestep = timestep 


	def add_frame(self, frame):
		image = np.array(frame)
		self.images.append(image) 

	def save_gif(self,  gif_name):
		imageio.mimsave(gif_name, self.images, duration=0.01)
		optimize(gif_name)


class DragonHandler:
	def __init__(self, settings):
		self.name = "dragon"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (self.size[0]/2, self.size[0]/4) 
		self.pen = Pen(self.size, self.startpos)

		self.animate = settings["animate"]
		self.gifmaker = GifMaker() if self.animate else None
		self.gif_factor = 16

	def execute_command(self, command):
		curr_heading = 	self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.length)
		elif command == "+":
			self.pen.right(self.angle)
		elif command == "-":
			self.pen.left(self.angle)

	def create_image(self, string, directory):
		self.pen.down()
		frame_num = 0
		for command in string:
			self.execute_command(command)
			if self.animate and frame_num%self.gif_factor==0:
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame)
			frame_num+=1

		self.pen.show()
		filename = self.name
		if self.animate:
			self.gifmaker.save_gif(directory + self.name + GIF_EXT)
			filename += GIF_EXT
		else:
			self.pen.save(directory + self.name + IMG_EXT)
			filename += IMG_EXT

		return  directory + filename

class KochHandler:
	def __init__(self, settings):
		self.name = "koch"
		self.length = settings["length"]
		self.angle = settings["angle"]
		self.size = (500, 500)
		self.startpos = (0, self.size[1])
		self.pen = Pen(self.size, self.startpos)

		self.animate = settings["animate"]
		self.gifmaker = GifMaker() if self.animate else None
		self.gif_factor = 8
 


	def execute_command(self, command):
		curr_heading = self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.length)
		elif command == "-":
			self.pen.right(self.angle)
		elif command == "+":
			self.pen.left(self.angle)

	def create_image(self, string, directory):
		self.pen.down()
		frame_num = 0
		for command in string:
			self.execute_command(command)
			if self.animate and frame_num%self.gif_factor==0:
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame)
			frame_num+=1

		self.pen.show()
		if self.animate:
			self.gifmaker.save_gif(directory + self.name + GIF_EXT)
			filename += GIF_EXT
		else:
			self.pen.save(directory + self.name + IMG_EXT)
			filename += IMG_EXT

		return  directory + filename
		

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

		self.animate = settings["animate"]
		self.gifmaker = GifMaker() if self.animate else None
		self.gif_factor = 8
 


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

	def create_image(self, string, directory):
		self.pen.down()
		frame_num = 0
		for command in string:
			self.execute_command(command)
			if self.animate and frame_num%self.gif_factor==0:
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame)
			frame_num+=1

		self.pen.show()
		if self.animate:
			self.gifmaker.save_gif(directory + self.name + GIF_EXT)
			filename += GIF_EXT
		else:
			self.pen.save(directory + self.name + IMG_EXT)
			filename += IMG_EXT

		return  directory + filename
		


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

		self.animate = settings["animate"]
		self.gifmaker = GifMaker() if self.animate else None
		self.gif_factor = 8
 

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

	def create_image(self, string, directory):
		self.pen.down()
		frame_num = 0
		for command in string:
			self.execute_command(command)
			if self.animate and frame_num%self.gif_factor==0:
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame)
			frame_num+=1

		self.pen.show()
		filename = self.name
		if self.animate:
			self.gifmaker.save_gif(directory + self.name + GIF_EXT)
			filename += GIF_EXT
		else:
			self.pen.save(directory + self.name + IMG_EXT)
			filename += IMG_EXT

		return  directory + filename
		

