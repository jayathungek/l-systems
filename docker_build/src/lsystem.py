class Generator:
	def __init__(self, settings):
		self.alphabet = settings["alphabet"]
		self.axiom = settings["axiom"]
		self.rules = settings["rules"]
		self.iterations = settings["iterations"]
		self.animate = settings["animate"]
		self.lsequence = []

	def generate(self):
		n = self.iterations
		sentence = self.axiom
		self.lsequence.append(self.axiom)
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
			self.lsequence.append(sentence)
			n -= 1
		if self.animate:
			return self.lsequence
		else:
			return [self.lsequence[-1]]
