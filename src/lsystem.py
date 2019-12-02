class Generator:
	def __init__(self, settings):
		self.alphabet = settings["alphabet"]
		self.axiom = settings["axiom"]
		self.rules = settings["rules"]
		self.iterations = settings["iterations"]
		self.animate = settings["animate"] 

	def generate(self):
		n = self.iterations
		sentence = self.axiom 
		while n > 0:
			new_sentence = ""
			for char in sentence:
				rule_found = False
				for rule in self.rules:
					if char == rule["in"]:
						new_sentence += rule["out"]
						rule_found = True
						break
				if not rule_found:
					new_sentence += char
			sentence = new_sentence 
			n -= 1
		return sentence
