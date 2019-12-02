from PIL import Image, ImageDraw
import math

class Pen:
	def __init__(self, image_dimensions, pen_pos=(0, 0)):
		self.pos = pen_pos
		self.heading = 0
		self.is_down = False
		self.bg = "#4C4C4C"
		self.colour = "#EC99B2"
		self.canvas_size = image_dimensions

		self.image = Image.new('RGBA', self.canvas_size, self.bg)
		self.drawing = ImageDraw.Draw(self.image)

	def forward(self, dist):
		newpos = ((dist * math.cos(self.heading)) + self.pos[0], (dist * math.sin(self.heading)) + self.pos[1])
		if self.is_down:
			self.drawing.line(self.pos + newpos, fill=self.colour)
		self.pos = newpos

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

	def set_colour(self, new_colour):
		self.colour = new_colour

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






