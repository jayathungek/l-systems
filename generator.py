from util import Util

class Generator:
	def __init__(self, settings, old=False):
		self.settings = settings
		self.old = old

	

	def generate(self):
		n = self.settings["iterations"]
		if not self.old:
			self.width = self.settings["w0"]
		sentence = self.settings["axiom"] 
		while n > 0:
			new_sentence = ""
			for char in sentence:
				rule_found = False
				for rule in self.settings["rules"]:
					if char == rule["in"]:
						new_sentence += rule["out"]
						rule_found = True
						break
				if not rule_found:
					new_sentence += char

			if not self.old:
				new_sentence = Util.replace_char(new_sentence, "s", self.settings["length"])
				new_sentence = Util.replace_char(new_sentence, "w", self.width)
				angle = Util.add_noise(self.settings["angle"], self.settings["angle_leeway"])
				new_sentence = Util.replace_char(new_sentence, "a", angle)
				self.width = self.width * pow(self.settings["q"], self.settings["e"])

			sentence = new_sentence 
			n -= 1
		return sentence

if __name__ == "__main__":
	import sys
	settings = sys.argv[1]
	g = Generator(settings)
	s = g.generate()
	print(s)
