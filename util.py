import random
import numpy as np
import json
import string

class Util:
	TRUTHY = ["yes", "true", "y", "1", "t"]
	FALSEY = ["no", "false", "n", "0", "f"]
	ALPHA  = string.ascii_lowercase

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
		r = hex(rgb[0])[2:].zfill(2)
		g = hex(rgb[1])[2:].zfill(2)
		b = hex(rgb[2])[2:].zfill(2)
		return "#" + r + g + b

	@staticmethod
	def lerp_colour(c1, c2, percent): 
	    if c1 == c2:
	    	return c1
	    
	    c1 = Util.hex_to_rgb(c1)
	    c2 = Util.hex_to_rgb(c2)

	    c1 = np.array(c1)
	    c2 = np.array(c2)
	    vector = c2-c1
	    c_new = c1 + vector * percent
	    h = Util.rgb_to_hex((int(c_new[0]), int(c_new[1]), int(c_new[2])))

	    if len(h) != 7:
	    	print((int(c_new[0]), int(c_new[1]), int(c_new[2])))
	    return h

	@staticmethod
	def get_settings_from_json_file(filename): 
		print("using settings file: " + filename)
		try:
			with open(filename, 'r') as f:
			    return json.load(f) 

		except json.decoder.JSONDecodeError as e:
			print ("Bad JSON format, fix errors in JSON file.")
			return
		except FileNotFoundError as e:
			print("File {} does not exist. Check file path for typos.".format(filename))
			return

	@staticmethod
	def get_settings_from_json(string): 
		print("using settings string: " + string)
		try:
			return json.loads(string) 

		except json.decoder.JSONDecodeError as e:
			print ("Bad JSON format, fix errors in JSON file.")
			return

	@staticmethod
	def isNumeric(string): 
		try:
			float(string)
			return True
		except ValueError:
			return False

	@staticmethod
	def isInteger(string): 
		try:
			int(string)
			return True
		except ValueError:
			return False

	@staticmethod
	def isBool(string):
		if (string.lower() not in Util.TRUTHY) and (string.lower() not in Util.FALSEY):
			return False
		return True

	@staticmethod
	def strToBool(string):
		if string.lower() in Util.TRUTHY:
			return True
		elif string.lower() in Util.FALSEY:
			return False

	@staticmethod
	def random_selection(l, exclude=[]):
		s = random.choice(l)
		while s in exclude:
			s = random.choice(l)
		return s

	@staticmethod
	def get_random():
		return random.random()

	@staticmethod
	def is_space(char):
		if char == "\n":
			return False
		else:
			return char.isspace()

	@staticmethod
	def clean_whitespace(string):
		string = string.strip()
		cleaned_string = ""
		in_ws = False
		for char in string:
			if Util.is_space(char):
				if in_ws:
					continue
				cleaned_string += " "
				in_ws = True
			else:
				cleaned_string += char
				in_ws = False
		return cleaned_string


	@staticmethod
	def to_snake_case(camel_string):
		idx = 0
		snaked_string = ""
		for char in camel_string:
			if char.isupper():
				if idx > 0:
					snaked_string += "_{}".format(char.lower())
				else:
					snaked_string += char.lower()
			else:
				snaked_string += char

			idx += 1

		return snaked_string

	@staticmethod
	def diff_list(l1, l2):
		larger = l1
		smaller = l2
		
		if len(l1) < len(l2):
			larger = l2
			smaller = l1

		diff = []
		for item in larger:
			if item not in smaller:
				diff.append(item)

		return diff

	@staticmethod
	def alpha_to_int(alpha_string):
		diff = ord("a")
		reversed_string = ''.join(reversed(alpha_string))
		final_sum = 0
		place = 0
		for char in reversed_string:
			num = ord(char) - diff
			final_sum += (num * pow(26, place))
			place += 1

		return final_sum

	@staticmethod
	def get_seed(seed_len):
		seed = ""
		for i in range(seed_len):
			seed += random.choice(Util.ALPHA)
		return seed

	@staticmethod
	def seed_random(seed):
		random.seed(seed)



if __name__ == "__main__":
	# c1 = "#e39046"
	# c2 = "#000000"
	# c3 = Util.lerp_colour(c1, c2, 0.3141598)
	# print(c3)
	# s = "1"
	# if Util.isBool(s):
	# 	print(Util.strToBool(s))
	print(Util.get_seed(6))

