import imageio
from pygifsicle import optimize
import numpy as np
import os

from pen import Pen
from util import Util
import params

IMG_EXT = ".png"
GIF_EXT = ".gif"


class GifMaker:
	def __init__(self, timestep=0.5):
		self.images = []
		self.timestep = timestep 


	def add_frame(self, frame):
		image = np.array(frame)
		self.images.append(image) 

	def save_gif(self,  gif_name):
		imageio.mimsave(gif_name, self.images, duration=0.01)
		# optimize(gif_name)

class PlantHandler:
	def __init__(self, settings):
		self.name = "plant"
		self.settings = settings  
		self.size = (500, 500)
		self.startpos = (self.size[0]/2, self.size[1])
		self.pen = Pen(self.size, self.settings["w0"], self.startpos) 
		self.pen.set_heading(-90)
		self.stack = []

		self.animate = settings["animate"]
		self.gifmaker = GifMaker() if self.animate else None
		self.gif_factor = 64
		self.leaf_steps = 20
		self.leaf_animation_steps = 4
		self.leaf_animation_linger_frames = 5
		self.leaf_stem = settings["length"]
		self.fruit_stem = settings["length"] * 4
		self.side = settings["length"] * 2
		self.linger_frames = 20
		self.start_colour = params.COLOURS[settings["start_colour"]]
		self.end_colour = params.COLOURS[settings["end_colour"]]
		self.fruit_colour = params.COLOURS[settings["fruit_colour"]]
		self.leaf_colour = params.COLOURS[settings["leaf_colour"]]
		self.fruit_radius = settings["length"]
		self.fruit_density = settings["fruit_density"]
		self.leaf_density = settings["leaf_density"]
		self.leaves = []
		self.finished_tree = settings["finished"]

	def get_colour_from_thickness(self, thickness):
		base_thickness = self.settings["w0"]
		r = thickness/base_thickness
		return Util.lerp_colour(self.end_colour, self.start_colour, r)
 


	def execute_command(self, command):
		curr_heading = self.pen.get_heading()
		if command == "F":
			self.pen.forward(self.settings["length"])
		elif command == "-":
			angle = Util.add_noise(self.settings["angle"], self.settings["angle_leeway"])
			angle *= Util.get_sign(0.9)
			self.pen.right(angle)
		elif command == "+":
			angle = Util.add_noise(self.settings["angle"], self.settings["angle_leeway"])
			angle *= Util.get_sign(0.9)
			self.pen.left(angle)
		elif command == "O":
			to_draw = Util.get_sign(self.fruit_density)
			if to_draw == -1:
				self.pen.draw_fruit(self.fruit_stem, self.fruit_radius, self.fruit_colour)
		elif command == "L":
			to_draw = Util.get_sign(self.leaf_density)
			if to_draw == -1:
				pen_heading = self.pen.get_heading()
				angle = Util.add_noise(pen_heading, 45)
				l = {"pos": self.pen.pos, "angle": angle}
				self.leaves.append(l) 
				# self.pen.draw_leaf(10, 10, angle, colour="#EA1CCC") 
		elif command == "[":
			self.pen.set_thickness(self.pen.thickness * self.settings["w_factor"])
			self.stack.append({"pos": self.pen.get_pos(), 
				"heading": self.pen.get_heading(),
				"thickness": self.pen.get_thickness()})
		elif command == "]":
			cmd = self.stack.pop()
			self.pen.up()
			self.pen.set_heading(cmd["heading"])
			self.pen.set_pos(cmd["pos"])
			self.pen.set_thickness(cmd["thickness"])
			new_colour = self.get_colour_from_thickness(self.pen.thickness)
			self.pen.set_colour(new_colour)
			self.pen.down()

	def draw_leaves(self, step, angle_offset=0):
		for leaf in self.leaves:
			self.pen.draw_leaf(self.leaf_stem, (step/self.leaf_steps)*self.side, leaf["angle"] + angle_offset, self.leaf_colour, leaf["pos"]) 
		f = self.pen.get_image()
		return f
		


	def create_image(self, string, directory):
		self.pen.down()
		self.pen.set_colour(self.start_colour)
		frame_num = 0
		for command in string:
			self.execute_command(command)
			if self.animate and (frame_num%self.gif_factor==0) and (not self.finished_tree):
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame)
			frame_num+=1

		base_frame = self.pen.get_image().copy()
		# self.gifmaker.add_frame(base_frame)

		if self.finished_tree:
			da = 5
			to_turn = da 
			for i in range(self.leaf_animation_steps):
				self.pen.set_base_image(base_frame) 
				if i < int(self.leaf_animation_steps/4):
					frame = self.draw_leaves(self.leaf_steps, to_turn)
					to_turn -= da
				elif i >= int(self.leaf_animation_steps/4) and i < int(self.leaf_animation_steps/2):
					frame = self.draw_leaves(self.leaf_steps, to_turn)
					to_turn += da
				elif i >= int(self.leaf_animation_steps/2) and i < int(self.leaf_animation_steps * 4/3):
					frame = self.draw_leaves(self.leaf_steps, to_turn)
					to_turn += da
				else:
					frame = self.draw_leaves(self.leaf_steps, to_turn)
					to_turn -= da

				for _ in range(self.leaf_animation_linger_frames):
					self.gifmaker.add_frame(frame)


		else:
			for step in range(self.leaf_steps):
				frame = self.draw_leaves(step)
				self.gifmaker.add_frame(frame)

			for i in range(self.linger_frames):
				frame = self.pen.get_image()
				self.gifmaker.add_frame(frame) 
		self.pen.show()
		filename = self.name
		if self.animate:
			self.gifmaker.save_gif(directory + self.name + GIF_EXT)
			filename += GIF_EXT
		else:
			self.pen.save(directory + self.name + IMG_EXT)
			filename += IMG_EXT

		return  directory + filename

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
		self.gif_factor = 64

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
		self.gif_factor = 64
 


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
		filename = self.name
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
		self.gif_factor = 64
 

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
		

