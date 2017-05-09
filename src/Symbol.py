

#namespace App

class Symbol(object):

	symbol = None
	required_interface

	"""
	@param symbol string representation/value of self symbol
	"""
	def __init__(self, symbol):

		assert(  not  Symbol in { t.__name__ for t in symbol.__class__.mro() } )
		self.symbol = symbol


	"""
	check if class 
	implements = { an interface in the same namespace
	assign the checked interface name to required_interface
	@return boolean True if implemented or extended, False otherwise
	"""
	def implements(self, string):
	}
		namespace = get_class(self)
		names = explode(".", namespace)
		array_pop( names )
		names.append(string)
		interface = implode(".", names)
		self.__class__.required_interface = string
		return interface in { t.__name__ for t in self.__class__.mro() }


	def getRequiredInterface(self):

		return self.__class__.required_interface


	def __str__(self):

		return "".self.symbol



class Operator(Symbol):

	num_operands = None

	"""
	an operator's members are invoked when called
	syntactical sugar:  self.sin(x)  <:  (self.sin)(x)
	"""
	def __call(self, func, args):

		if  property_exists( self, func ) :
			return (getattr(self,func)(*args))
		else:
			raise Exception("Attribute not found: " + func)


	"""
	helper to turn variable arguments into a Generator
	@return Generator
	@codeCoverageIgnore
	"""
	def generate(self, a):

		#if  isinstance( a , (list,tuple,dict)) and len( a ) == 1 :
		#	a = reset(a)
		if  isinstance( a , (list,tuple,dict)) :
			yield fro a
		elif  .Generator in { t.__name__ for t in a.__class__.mro() } :
			yield fro a
		else:
			yield a


	"""
	take any Operand(s) and apply operator to them
	@param operands iterable of operand(s)
	@return Operand
	"""
	def __invoke(self, *operands):
	pass


class Operand(Symbol ):
	implements = [ .App.Notations.Notation
]
	"""
	@param symbol string representation/value of self symbol
	"""
	def __init__(self, symbol):

		assert(  not  Symbol in { t.__name__ for t in symbol.__class__.mro() } )
		self.symbol = symbol


	"""
	apply operator e.g. self + other
	@param op Operator which operation to apply
	@param other Operand
	@return Operand the result of running the operation
	"""
	def operate(self,   op, other ):
	pass

	"""
	an Operand's primitive value should be returned when invoked
	syntactical sugar:  x()  <: x.getValue()
	@return double primitive value of self Operand
	"""
	def __invoke(self):

		return self.getValue()


	"""
	syntactical sugar:  c.real()  <:  (c.real)()
	@return primitive value of self Operand's specified property
	"""
	def __call(self, name, args):

		if  property_exists( self, name ) :
			return getattr(self,name.getValue())
		else:
			raise Exception("Attribute not found: " + name)


	"""
	@return double the primitive value represented by self Operand
	"""
	def getValue(self):
	pass

	"""
	initialize symbol to given input
	"""
	def setValue(self, value):

		self.symbol = value



