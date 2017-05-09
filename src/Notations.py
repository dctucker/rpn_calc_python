
import math, re
#namespace App.Notations

class Notation(object):

	@classmethod
	def regex(cls):
		pass

class Regex(Notation):

	"""
	@param string string to pattern-match, or None to return pattern
	@return string regex pattern or boolean indicating string matched
	"""
	@classmethod
	def regex(cls, string=None):
		pattern = cls.pattern()
		if( string is None ):
			return pattern
		matches = re.match(pattern, string)
		if matches:
			ret = [string]
			for m in matches.groups():
				ret.append(m)
			return ret
		else:
			return None

	"""
	@return string of regular expression to use
	"""
	@classmethod
	def pattern(cls):
		return "^.*$"



class Complex(Regex):

	@classmethod
	def pattern(cls):
		return '^((-?[0-9.]+)([+-]))?(-?[0-9.]+)?i'



class PolarComplex(Regex):

	@classmethod
	def pattern(cls):
		return '^(-?[0-9.]+)cis(-?[0-9.]+)deg'



class Degrees(Regex):

	@classmethod
	def pattern(cls):
		return '^(-?[0-9.]+)deg'

	def degSymbol(self, number):

		return math.degrees(number)+"deg"



class Alphabetic(Regex):

	@classmethod
	def pattern(cls):
		return "^[+-]?[^0-9]+"



class Base(Regex):

	"""
	@param integer numeric
	@return string token representing the given integer in self base
	"""
	def baseSymbol(self, integer):

		sign ='-'  if  ( integer < 0 ) else  ''
		return sign+self.__class__.prefix.base_convert( abs(integer), 10, self.__class__.base )


	@classmethod
	def pattern(cls):
		chars = "0-"
		if  cls.base > 10 :

			chars += "9A-"+chr(54+cls.base)
			chars +=  "a-"+chr(86+cls.base)

		else:

			chars += str(cls.base - 1)

		return "^(-?)("+cls.prefix+")([chars]+)"



class Decimal(Base):

	prefix = ""
	base = 10
	@classmethod
	def pattern(cls):
		return '^(-?[0-9.]+)$'



class Octal(Base):

	prefix = "o"
	base = 8


class Hexadecimal(Base):

	prefix = "0x"
	base = 16


class Binary(Base):

	prefix = "b"
	base = 2

