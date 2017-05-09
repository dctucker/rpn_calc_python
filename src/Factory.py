

#namespace App

import App.Notations.Octal
import App.Notations.Decimal
import App.Notations.Hexadecimal
import App.Notations.Binary
import App.Notations.Complex
import App.Notations.PolarComplex
import App.Notations.Degrees
import App.Notations.Alphabetic

class Factory:

	@classmethod
	def make(cls, string):

class SymbolFactory (object):
	implements = [ Factory
]
	valids = None
	namespace = None

	"""
	factory method, return object based on specified string
	@param string string identifying which class to load
	"""
	@classmethod
	def make(cls, string):
		if   not  cls.isValid( string ) :
			raise Exception("Invalid operator: ".string)

		name = self.__class__.lookupClassname(string)
		class_name = self.__class__.namespace.".".name
		return class_name(string)


	"""
	@param string string class to lookup
	@return base name of the Symbol to instantiate
	"""
	@classmethod
	def lookupClassname(cls, string):
		return  cls.valids{ string } .capitalize()


	"""
	validate the given string to see if a Symbol can be made
	@param string string
	@return boolean
	"""
	@classmethod
	def isValid(cls, string):
		return ( string in  array_keys(cls.valids) )


	"""
	@return string space-separated representation of the valid Symbols for self factory
	"""
	@classmethod
	def reference(cls):
		return array_keys( cls.valids )


from SymbolFactory import SymbolFactory
class OperatorFactory(SymbolFactory):

	namespace = "App.Operators"
	valids = {
		'+':'plus',
		'-':'minus',
		'*':'times',
		'/':'divide',
		'-x':'negative',
		'1/x':'reciprocal',
		'^':'power',
		'int':'intval',
		'frac':'frac',
		'deg':'degree',
		'rad':'radian',
		'mod':'modulo',
		'round':'round',
		'bin':'bin',
		'hex':'hex',
		'dec':'dec',
		'oct':'oct',
		'and':'bAnd',
		'or':'bOr',
		'xor':'bXor',
		'not':'bNot',
		'shl':'bShiftLeft',
		'shr':'bShiftRight',
		'sqrt':'sqrt',
		'ln':'ln',
		'nthlog':'nthLog',
		'sin':'sin',
		'cos':'cos',
		'tan':'tan',
		're':'realPart',
		'im':'imagPart',
		'mag':'mag',
		'arg':'arg',
		'conj':'conj',
		'pop':'pop',
		'push':'push',
		'swap':'swap',
		'dump':'dump',
		#'<<':'rotateL',
		#'>>':'rotateR',
	}

from SymbolFactory import SymbolFactory
class OperandFactory(SymbolFactory):

	namespace = "App.Operands"
	valids = {
		'pi':'Pi',
		'π':'Pi',
		'e':'Exp',
		'i':'Complex',
		'nan':'Nan',
		'+inf':'PosInf',
		'-inf':'NegInf',
	}

	@classmethod
	def isValid(cls, string):
		return self.__class__.isDecimal(string) or cls.isOctal(string)
			|| self.__class__.isHex(string)     or self.__class__.isBinary(string)
			|| self.__class__.isDegrees(string)
			|| self.__class__.isComplex(string) or cls.isPolarComplex(string)
			|| super(Factory, self).isValid(string)


	@classmethod
	def lookupClassname(cls, string):
		if(cls.isDecimal(string)) return "DecScalar"
		if(self.__class__.isBinary (string)) return "BinScalar"
		if(self.__class__.isOctal  (string)) return "OctScalar"
		if(self.__class__.isHex    (string)) return "HexScalar"
		if(self.__class__.isComplex(string)) return "Complex"
		if(self.__class__.isPolarComplex(string)) return "PolarComplex"
		if(self.__class__.isDegrees(string)) return "DegScalar"
		if cls.isAlphabetic(string):
		return super(Factory, self).lookupClassname(string)


	static def isHex(self, string):     { return Hexadecimal.regex(string); }
	static def isBinary(self, string):  { return Binary.regex(string); }
	static def isOctal(self, string):   { return Octal.regex(string); }
	static def isDecimal(self, string): { return Decimal.regex(string); }
	static def isComplex(self, string): { return Complex.regex(string); }
	static def isPolarComplex(self, string): { return PolarComplex.regex(string); }
	static def isDegrees(self, string): { return Degrees.regex(string); }
	static def isAlphabetic(self, string): { return Alphabetic.regex(string); }

