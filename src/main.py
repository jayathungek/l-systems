from lsystem import Generator
import json
import sys 
import error
import graphics.handlers as gh
from graphics.handlers import Util

DEFAULT_IMG_DIR = "../img/"
REQUIRED_FIELDS = ["alphabet", "axiom", "rules", "iterations", "animate", "graphics_class"]
ERROR_CODES = {
	1: "NoSettingsPassed",
	2: "TooManyFilesPassed",
	3: "BadJSONFormat",
	4: "NoGraphicsHandler",
	5: "FileDoesNotExist",
	6: "MissingRequiredField",
	7: "SymbolNotInAlphabet",
	8: "IterationsCannotBeNegative"
}

#Global variables
SETTINGS = {}
HANDLER_INSTANCE = None

def print_help():
	msg= """lsystems help
-------------------------------------------
Usage: python main.py settings
	where settings is a JSON file whose object
	has the following mandatory fields:
	{
		'alphabet': [...],
		'axiom': string,
		'iterations': int,
		'graphics_class': string,
		'rules': [...]
	}

	'alphabet' is a list of ALL valid characters
	that are allowed in the L-system
	 
	'axiom' is the starting string of the
	L-System, and must be composed of valid 
	characters
	 
	'iterations' is an integer that defines how
	many times the L-system will evolve
	 
	'graphics_class' is the name of the class in
	graphics/handlers.py that controls how to
	draw the output from the L-system
	 
	'rules' is a list of rule objects that define
	how to replace strings from the previous
	iteration. A rule object is defined as:
	{
		 'in': string,
		 'out': string
	}
	where 'in' is the string to match and 'out'
	is its replacement string

For examples of this in practice, see the
examples in graphics/settings"""
	   
	print(msg)

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

def get_settings_from_json(filename):
	global SETTINGS
	print("using settings file: " + filename)
	try:
		with open(filename, 'r') as f:
		    SETTINGS = json.load(f) 
	except json.decoder.JSONDecodeError as e:
		print ("Bad JSON format, fix errors in JSON file.")
		return
	except FileNotFoundError as e:
		print("File {} does not exist. Check file path for typos.".format(filename))
		return

def import_handler(graphics_class):
	global HANDLER_INSTANCE
	try:
		handler = getattr(gh, graphics_class)
		HANDLER_INSTANCE = handler(SETTINGS)
	except AttributeError as e:
		print("Graphics handler {} does not exist. Select one that does.".format(graphics_class))
		return

def out(lstrings, handler, outfile=DEFAULT_IMG_DIR):
	handler.create_image(lstrings, outfile)


def print_error(err):
	msg = "There was a problem with your command: " 
	msg += ERROR_CODES[err]
	print(msg)

def parse_args(args):
	if len(args) != 2:
		raise error.IncorrectArgsNumberError(len(args))

	err = get_settings_from_json(args[1])

	err = import_handler(SETTINGS["graphics_class"])

def validate_string(string, alphabet):
	for symbol in string:
		if symbol not in alphabet:
			raise error.SymbolNotInAlphabetError(symbol, alphabet)

def validate_input():
	missing = get_missing_fields(REQUIRED_FIELDS, SETTINGS.keys())
	if len(missing) > 0:
		raise error.MissingRequiredFieldsError(missing)

	alphabet = SETTINGS["alphabet"]
	axiom = SETTINGS["axiom"]
	rules = SETTINGS["rules"]
	iterations = SETTINGS["iterations"]
	
	validate_string(axiom, alphabet)		

	for rule in rules:
		validate_string(rule["in"], alphabet)
		validate_string(rule["out"], alphabet)

	if iterations < 0:
		raise error.NegativeFieldError(iterations)

	return 0


def main():
	args = sys.argv
	try:
		parse_args(args)
		validate_input()
	except error.Error as e:
		print (e.message)
		return
	
	lsg = Generator(SETTINGS)
	lstrings = lsg.generate()
	out(lstrings, HANDLER_INSTANCE)


if __name__ == "__main__": main()