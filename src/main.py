from lsystem import Generator
import json
import sys 
import graphics.handlers as gh

def get_settings_from_json(filename):
	settings = {}
	try:
		with open(filename, 'r') as f:
		    settings = json.load(f)
	except Exception as e:
		print("Could not open json file: "+str(e))
	return settings

def draw(lstrings, handler):
	handler.draw(lstrings)

def main():
	settings = get_settings_from_json(sys.argv[1])
	lsg = Generator(settings)
	lstrings = lsg.generate() 
	handler = getattr(gh, settings["graphics_class"])
	handler_instance = handler(settings)
	draw(lstrings, handler_instance)


if __name__ == "__main__": main()