import random
import numpy as np
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

	@staticmethod
	def add_noise(angle, amount):
		r = random.random()
		sign = 1 if r > 0.5 else -1
		delta_angle =  amount * r
		return angle + (sign * delta_angle)

	@staticmethod
	def get_sign(p=0.5):
		r = random.random()
		return 1 if r > p else -1

	@staticmethod
	def replace_char(original, to_replace, replacement):
		final = ""
		for char in original:
			if char == to_replace:
				final += str(replacement)
			else:
				final += char

		return final

	@staticmethod
	def hex_to_rgb(hex):
		r = int(hex[1:3], 16)
		g = int(hex[3:5], 16)
		b = int(hex[5:], 16)
		return (r, g, b)

	@staticmethod
	def rgb_to_hex(rgb):
		r = hex(rgb[0])[2:]
		g = hex(rgb[1])[2:]
		b = hex(rgb[2])[2:]
		return "#" + r + g + b

	@staticmethod
	def lerp_colour(c1, c2, percent):
	    '''assumes color is rgb between (0, 0, 0) and (255, 255, 255)'''
	    c1 = Util.hex_to_rgb(c1)
	    c2 = Util.hex_to_rgb(c2)

	    c1 = np.array(c1)
	    c2 = np.array(c2)
	    vector = c2-c1
	    c_new = c1 + vector * percent
	    return Util.rgb_to_hex((int(c_new[0]), int(c_new[1]), int(c_new[2])))


if __name__ == "__main__":
	c1 = "#FFFFFF"
	c2 = "#000000"
	c3 = Util.lerp_colour(c1, c2, 0.5)
	print(c3)