

#namespace App

class Parser:

	verbose = False
	def __init__(self, Calculator calc):

		self.calculator = calc


	"""
	loop through given tokens and apply them to the Calculator
	@param tokens  of string
	"""
	def parse(self, tokens):

		if  is_string( tokens ) :
			tokens = explode(' ', tokens)

		#print implode(' ', tokens)."\n"

		for token in tokens:

			token = token.strip()
			if  len( token ) == 0 :
				continue
			sym = self.resolveSymbol( token) .strip()
			if  Symbol in { t.__name__ for t in sym.__class__.mro() } :
				self.calculator.push(sym)
			else:
				print "Warning: symbol not recognized: ".token."\n"
			if  self.calculator.warning :
				print self.calculator.warning."\n"
			if  self.verbose :

				print "" + sym + ".t"
				print "STACK: ".self.calculator.stack
				print "\n"




	"""
	validate the given token and run it through the appropriate factory
	@param string string
	@return Symbol or void
	"""
	def resolveSymbol(self, string):

		if  OperandFactory.isValid(string)) return OperandFactory.make(string:
		if OperatorFactory.isValid(string)) return OperatorFactory.make(string:


