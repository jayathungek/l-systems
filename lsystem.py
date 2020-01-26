from generator import Generator
import json
import sys 
import error

import handlers as gh 
from util import Util
import params

class LSystem:
	def __init__(self, settings, random=False, cmd=True ):
		self.DEFAULT_IMG_DIR = "./"
		self.REQUIRED_FIELDS = ["alphabet", "axiom", "rules", "iterations", "animate", "graphics_class"] 
		self.settings = None 
		self.handler = None 

		if cmd:
			self.get_settings_from_json_file(settings)
		else:
			self.get_settings_from_json(settings)

		if random:
			self.randomise_settings()

		self.import_handler(self.settings["graphics_class"])



	def import_handler(self, graphics_class): 
		try:
			handler = getattr(gh, graphics_class)
			self.handler = handler(self.settings)
		except AttributeError as e:
			print(e)
			print("Graphics handler {} does not exist. Select one that does.".format(graphics_class))
			return

	@staticmethod
	def get_missing_fields(original, test):
		diff = []
		for field in test:
			if field not in original:
				diff.append(field)

		missing = []
		for field in diff:
			if field in original:
				missing.append(field)

		return missing


	
	@staticmethod
	def validate_string(string, alphabet):
		for symbol in string:
			if symbol not in alphabet:
				raise error.SymbolNotInAlphabetError(symbol, alphabet)


	def out(self, lstrings, handler):
		outfile = self.DEFAULT_IMG_DIR
		created_filename = handler.create_image(lstrings, outfile)
		return created_filename

	def get_settings_from_json_file(self, filename): 
		print("using settings file: " + filename)
		try:
			with open(filename, 'r') as f:
			    self.settings = json.load(f) 

		except json.decoder.JSONDecodeError as e:
			print ("Bad JSON format, fix errors in JSON file.")
			return
		except FileNotFoundError as e:
			print("File {} does not exist. Check file path for typos.".format(filename))
			return

	def get_settings_from_json(self, string): 
		print("using settings string: " + string)
		try:
			self.settings = json.loads(string) 

		except json.decoder.JSONDecodeError as e:
			print ("Bad JSON format, fix errors in JSON file.")
			return



	def validate_input(self):
		missing = LSystem.get_missing_fields(self.REQUIRED_FIELDS, self.settings.keys())
		if len(missing) > 0:
			raise error.MissingRequiredFieldsError(missing)

		alphabet = self.settings["alphabet"]
		axiom = self.settings["axiom"]
		rules = self.settings["rules"]
		iterations = self.settings["iterations"]
		
		LSystem.validate_string(axiom, alphabet)		

		for rule in rules:
			LSystem.validate_string(rule["in"], alphabet)
			LSystem.validate_string(rule["out"], alphabet)

		if iterations < 0:
			raise error.NegativeFieldError(iterations)

		return 0

	def run(self):
		try: 
			self.validate_input()
		except error.Error as e:
			print (e.message)
			return
		
		lsg = Generator(self.settings, old=True)
		lstrings = lsg.generate()
		image = self.out(lstrings, self.handler)
		return image

	def randomise_settings(self):
		colours = list(params.COLOURS.keys())

		self.settings["iterations"] = Util.random_selection([4, 5])
		self.settings["angle"] = Util.add_noise(self.settings["angle"], 10) 
		self.settings["w0"] = Util.random_selection([10, 15, 20, 25])

		leaf_d = Util.get_random()
		fruit_d = leaf_d/20
		self.settings["leaf_density"] = leaf_d
		self.settings["fruit_density"] = fruit_d

		self.settings["leaf_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		self.settings["fruit_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		self.settings["start_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		self.settings["end_colour"] = Util.random_selection(colours, exclude=["gray", "grey"]) 
 

if __name__ == "__main__":
	settings = sys.argv[1]
	lsg = LSystem(settings, random=True)
	lsg.run()

	# s = "!(w)F(s)+(a)[[X]-(a)X]-(a)F(s)[-(a)F(s)X]+(a)X"
	# s = LSystem.replace_char(s, "a", str(25))
	# s = LSystem.replace_char(s, "w", str(30))
	# s = LSystem.replace_char(s, "s", str(5))
	# print(s)















# def print_help():
# 	msg= """lsystems help
# -------------------------------------------
# Usage: python main.py settings
# 	where settings is a JSON file whose object
# 	has the following mandatory fields:
# 	{
# 		'alphabet': [...],
# 		'axiom': string,
# 		'iterations': int,
# 		'graphics_class': string,
# 		'rules': [...]
# 	}

# 	'alphabet' is a list of ALL valid characters
# 	that are allowed in the L-system
	 
# 	'axiom' is the starting string of the
# 	L-System, and must be composed of valid 
# 	characters
	 
# 	'iterations' is an integer that defines how
# 	many times the L-system will evolve
	 
# 	'graphics_class' is the name of the class in
# 	graphics/handlers.py that controls how to
# 	draw the output from the L-system
	 
# 	'rules' is a list of rule objects that define
# 	how to replace strings from the previous
# 	iteration. A rule object is defined as:
# 	{
# 		 'in': string,
# 		 'out': string
# 	}
# 	where 'in' is the string to match and 'out'
# 	is its replacement string

# For examples of this in practice, see the
# examples in graphics/settings"""
	   
# 	print(msg)