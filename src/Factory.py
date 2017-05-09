# -*- encoding: utf-8 -*-

#namespace App

from Notations import Octal
from Notations import Decimal
from Notations import Hexadecimal
from Notations import Binary
from Notations import Complex
from Notations import PolarComplex
from Notations import Degrees
from Notations import Alphabetic

class Factory:

	@classmethod
	def make(cls, string):
		pass

class SymbolFactory (object, Factory):
	valids = None
	namespace = None

	"""
	factory method, return object based on specified string
	@param string string identifying which class to load
	"""
	@classmethod
	def make(cls, string):
		if not cls.isValid( string ) :
			raise Exception("Invalid operator: "+string)

		name = cls.lookupClassname(string)
		module = __import__(cls.namespace)
		class_name = getattr(module, name)
		return class_name(string)


	"""
	@param string string class to lookup
	@return base name of the Symbol to instantiate
	"""
	@classmethod
	def lookupClassname(cls, string):
		return  cls.valids[ string ].capitalize()


	"""
	validate the given string to see if a Symbol can be made
	@param string string
	@return boolean
	"""
	@classmethod
	def isValid(cls, string):
		return string in cls.valids.keys()


	"""
	@return string space-separated representation of the valid Symbols for self factory
	"""
	@classmethod
	def reference(cls):
		return cls.valids.keys()


class OperatorFactory(SymbolFactory):

	namespace = "Operators"
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

class OperandFactory(SymbolFactory):

	namespace = "Operands"
	valids = {
		'pi':'Pi',
		u'π':'Pi',
		'e':'Exp',
		'i':'Complex',
		'nan':'Nan',
		'+inf':'PosInf',
		'-inf':'NegInf',
	}

	@classmethod
	def isValid(cls, string):
		return cls.isDecimal(string) or cls.isOctal(string) \
			or cls.isHex(string)     or cls.isBinary(string) \
			or cls.isDegrees(string) \
			or cls.isComplex(string) or cls.isPolarComplex(string) \
			or string in cls.valids.keys()


	@classmethod
	def lookupClassname(cls, string):
		if(cls.isDecimal(string)):return "DecScalar"
		if(cls.isBinary (string)):return "BinScalar"
		if(cls.isOctal  (string)):return "OctScalar"
		if(cls.isHex    (string)):return "HexScalar"
		if(cls.isComplex(string)):return "Complex"
		if(cls.isPolarComplex(string)):return "PolarComplex"
		if(cls.isDegrees(string)):return "DegScalar"
		if cls.isAlphabetic(string):
			return super(SymbolFactory, self).lookupClassname(string)


	@classmethod
	def isHex(self, string):
		return Hexadecimal.regex(string)
	@classmethod
	def isBinary(self, string):
		return Binary.regex(string)
	@classmethod
	def isOctal(self, string):
		return Octal.regex(string)
	@classmethod
	def isDecimal(self, string):
		return Decimal.regex(string)
	@classmethod
	def isComplex(self, string):
		return Complex.regex(string)
	@classmethod
	def isPolarComplex(self, string):
		return PolarComplex.regex(string)
	@classmethod
	def isDegrees(self, string):
		return Degrees.regex(string)
	@classmethod
	def isAlphabetic(self, string):
		return Alphabetic.regex(string)

