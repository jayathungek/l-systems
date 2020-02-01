from PIL import Image, ImageDraw
import math

import params
from util import Util

class Pen:
	def __init__(self, image_dimensions, thickness, pen_pos=(0, 0)):
		self.pos = pen_pos
		self.heading = 0
		self.is_down = False
		self.bg = params.COLOURS["dark_gray"]
		self.colour = params.COLOURS["pink"]
		self.canvas_size = image_dimensions
		self.thickness = thickness

		self.image = Image.new('RGBA', self.canvas_size, self.bg)
		self.drawing = ImageDraw.Draw(self.image)

	def forward(self, dist):
		newpos = ((dist * math.cos(self.heading)) + self.pos[0], (dist * math.sin(self.heading)) + self.pos[1])
		if self.is_down:
			self.drawing.line(self.pos + newpos, fill=self.colour, width=int(self.thickness))
		self.pos = newpos

	def draw_fruit(self, stem, r, colour, pos=None):
		if pos is None:
			pos = self.pos

		newpos = (pos[0], pos[1] + stem)
		self.drawing.line(pos + newpos, fill=self.colour, width=int(self.thickness))
		
		x = (newpos[0] - r, newpos[1] - r)
		y = (newpos[0] + r, newpos[1] + r)
		self.drawing.ellipse([x, y], fill=colour)

	def draw_leaf(self, stem, side, angle, colour, pos=None):
		if pos is None:
			pos = self.pos

		fill_colour = colour
		self.make_darker(0.2)

		cur_pos = pos
		self.set_pos(pos)
		cur_heading = self.heading
		leaf_int_angle = 30
		polygon = []

		

		self.set_heading(angle)
		self.forward(stem)
		polygon.append(self.pos)
		self.up()

		self.left(leaf_int_angle)
		self.forward(side)
		polygon.append(self.pos)

		self.right(2 * leaf_int_angle)
		self.forward(side)
		polygon.append(self.pos)

		self.right(4 * leaf_int_angle)
		self.forward(side)
		polygon.append(self.pos) 

		self.set_pos(cur_pos)
		self.set_heading(cur_heading)

		self.down()

		self.set_colour(fill_colour)

		line = Util.lerp_colour(self.get_colour(), params.COLOURS["black"], 0.2)
		self.drawing.polygon(polygon, fill=self.get_colour(), outline=line)





	def left(self, heading):
		radians = (heading * math.pi)/180.0
		self.heading -= radians

	def right(self, heading):
		radians = (heading * math.pi)/180.0 
		self.heading += radians 

	def up(self):
		self.is_down = False

	def down(self):
		self.is_down = True

	def set_pos(self, newpos):
		self.pos = newpos

	def set_heading(self, new_heading):
		radians = (new_heading * math.pi)/180.0 
		self.heading = radians

	def get_pos(self):
		return self.pos

	def get_heading(self):
		degrees = (self.heading * 180)/math.pi
		return degrees

	def set_thickness(self, new_thickness):
		self.thickness = new_thickness

	def get_thickness(self):
		return self.thickness

	def set_colour(self, new_colour):
		self.colour = new_colour

	def get_colour(self):
		return self.colour

	def make_darker(self, amount):
		black = "#000000"
		new_colour = Util.lerp_colour(self.get_colour(), black, amount)
		self.set_colour(new_colour)


	def set_bg(self, new_bg):
		self.bg = new_bg


	def set_canvas_size(self, size):
		self.canvas_size = size
		self.image = Image.new('RGBA', self.canvas_size, self.bg)
		self.drawing = ImageDraw.Draw(self.image)

	def show(self):
		self.image.show()

	def save(self, filename):
		self.image.save(filename, 'PNG')

	def get_image(self):
		return self.image






