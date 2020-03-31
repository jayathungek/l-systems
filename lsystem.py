from generator import Generator
import json
import sys 
import error

import handlers as gh 
from util import Util
import params

class LSystem:
	VALID_FIELDS = ["iterations", "start_colour", "end_colour", "fruit_colour", "leaf_colour", "length", "fruit_density", "leaf_density", "seed"]
	def __init__(self, settings, random=False, cmd=True, exclude=[]):
		self.DEFAULT_IMG_DIR = "./"
		self.REQUIRED_FIELDS = ["alphabet", "axiom", "rules", "iterations", "animate", "graphics_class", "seed"]
		self.settings = None 
		self.handler = None 

		if cmd:
			self.get_settings_from_json_file(settings)
		else:
			# self.get_settings_from_json(settings)
			self.settings = settings

		if random:
			self.randomise_settings(exclude)

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

	def randomise_settings(self, exclude):

		colours = list(params.COLOURS.keys())
		leaf_d = round(Util.get_random(), 2)
		fruit_d = round(leaf_d/20, 2)
		tree_l = round(Util.get_random(), 2)
		length = round(tree_l * 10, 2) if tree_l > 0 else 1  


		self.settings["angle"] = Util.add_noise(self.settings["angle"], 10) 
		self.settings["w0"] = Util.random_selection(params.W0)

		if "iterations" not in exclude:
			self.settings["iterations"] = Util.random_selection([4, 5])
		
		if "leaf_density" not in exclude:
			self.settings["leaf_density"] = leaf_d
		
		if "fruit_density" not in exclude:
			self.settings["fruit_density"] = fruit_d
		
		if "leaf_colour" not in exclude:
			self.settings["leaf_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		
		if "fruit_colour" not in exclude:
			self.settings["fruit_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		
		if "start_colour" not in exclude:
			self.settings["start_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])
		
		if "end_colour" not in exclude:
			self.settings["end_colour"] = Util.random_selection(colours, exclude=["gray", "grey"])

		if "length" not in exclude:
			self.settings["length"] = length 
 
	def get_settings_string(self):
		tree_l = round(self.settings["length"], 2)
		fruit_d = round(self.settings["fruit_density"], 2)
		leaf_d = round(self.settings["leaf_density"], 2)

		string = "SETTINGS\n"
		string += "iterations:{}\n".format(str(self.settings["iterations"]))
		string += "start:{}\n".format(self.settings["start_colour"])
		string += "end:{}\n".format(self.settings["end_colour"])
		string += "fruit:{}\n".format(self.settings["fruit_colour"])
		string += "leaf:{}\n".format(self.settings["leaf_colour"])
		string += "scale:{}\n".format(str(tree_l))
		string += "fruit_density:{}\n".format(str(fruit_d))
		string += "leaf_density:{}\n".format(str(leaf_d))
		string += "seed:{}".format(self.settings["seed"])
		return string

if __name__ == "__main__":
	settings = sys.argv[1]
	lsg = LSystem(settings, random=True)
	lsg.run()
 