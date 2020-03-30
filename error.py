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

class MalformedSettingsError(Error):
	def __init__(self, line_num):
		self.message = "Bad formatting on line {} of settings.".format(line_num)

class ParameterError(Error):
	def __init__(self, parameter, passed_value, rule):
		self.message = "Bad argument for {}: {}. {}".format(parameter, passed_value, rule)

class ParameterDoesNotExistError(Error):
	def __init__(self, parameter):
		self.message = "Parameter {} does not exist".format(parameter)

class ResponseTimeoutError(Error):
	def __init__(self):
		self.message = "Took too long to generate the tree."