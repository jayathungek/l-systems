from colour import RGB_TO_COLOR_NAMES as palette
from util import Util

COLOURS = {}

for val_rgb in palette.keys():
	val_hex = Util.rgb_to_hex(val_rgb)
	alt_colour_names = palette[val_rgb]
	for colour in alt_colour_names:
		colour = Util.to_snake_case(colour)
		COLOURS[colour] = val_hex

COLOURS['teal'] = '#008080'

GRADIENTS = {
	"transrights": {"start": "blue", "end": "pink"},
	"": {"start": "pink", "end": "white"},
	"fiftyshades": {"start": "gray", "end": "white"},
	"icicle": {"start": "blue", "end": "white"},
	"pumpkin": {"start": "orange", "end": "white"},
	"garfield": {"start": "orange", "end": "black"},
	"": {"start": "", "end": ""},
	 
}

TIMEOUT = 20

SEEDLEN = 6

def main():
	print(COLOURS)
if __name__=="__main__": main()