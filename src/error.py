class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class IncorrectArgsNumberError(Error):
	def __init__(self, num_args):
		self.message = "Wrong number of arguments: {}. Expected 1 commandline argument.".format(num_args)

class NoGraphicsHandlerError(Error):
	def __init__(self, handler):
		self.message = "Graphics handler {} does not exist. Select one that does.".format(handler)

class MissingRequiredFieldsError(Error):
	def __init__(self, fields):
		self.message = "The following required fields are missing from the settings JSON: {}".format(", ".join(fields))

class SymbolNotInAlphabetError(Error):
	def __init__(self, symbol, alphabet):
		self.message = "Symbol '{}' does not exist in the alphabet '{}'. Use only symbols from within the predefined alphabet.".format(symbol, alphabet)

class NegativeFieldError(Error):
	def __init__(self, field, number):
		self.message = "Invalid number for field {} : {}. Number cannot be negative".format(field, number)
