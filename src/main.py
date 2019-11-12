from lsystem import Generator
import json
import sys 
import graphics.handlers as gh

DEFAULT_IMG_DIR = "../img/"
ERROR_CODES = {
	1: "NoSettingsPassed",
	2: "TooManyFilesPassed",
	3: "BadJSONFormat",
	4: "NoGraphicsHandler",
	5: "FileDoesNotExist"
}

#Global variables
SETTINGS = {}
HANDLER_INSTANCE = None

def get_settings_from_json(filename):
	global SETTINGS 
	try:
		with open(filename, 'r') as f:
		    SETTINGS = json.load(f) 
	except json.decoder.JSONDecodeError as e:
		return 3
	except FileNotFoundError as e:
		return 5
	return 0

def import_handler(graphics_class):
	global HANDLER_INSTANCE
	try:
		handler = getattr(gh, graphics_class)
		HANDLER_INSTANCE = handler(SETTINGS)
	except AttributeError as e:
		return 4

	return 0

def out(lstrings, handler, outfile=DEFAULT_IMG_DIR):
	handler.create_image(lstrings, outfile)

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

def print_error(err):
	msg = "There was a problem with your command: " 
	msg += ERROR_CODES[err]
	print(msg)

def parse_args(args):
	if len(args) == 1:
		return 1
	elif len(args) > 2:
		return 2

	err = get_settings_from_json(args[1])
	if err != 0:
		return err

	err = import_handler(SETTINGS["graphics_class"])
	if err != 0:
		return err

	return 0

def main():
	args = sys.argv
	err = parse_args(args)
	if err != 0:
		print_error(err)
		# print_help()
		exit()

	lsg = Generator(SETTINGS)
	lstrings = lsg.generate()
	out(lstrings, HANDLER_INSTANCE)


if __name__ == "__main__": main()