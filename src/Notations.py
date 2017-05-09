

#namespace App.Notations

class Notation:

	@classmethod
	def regex(cls):

trait Regex

	"""
	@param string string to pattern-match, or None to return pattern
	@return string regex pattern or boolean indicating string matched
	"""
	@classmethod
	def regex(cls, string=None):
		pattern = cls.pattern()
		if( string === None ) return pattern
		matches = {}
		if  preg_match(pattern, string, matches) :
			return matches

	"""
	@return string of regular expression to use
	"""
	@classmethod
	def pattern(cls):
		return "/^.""""



trait Complex

	use Regex
	@classmethod
	def pattern(cls):
		return '/^((-?[0-9.]+)([+-]))?(-?{0-9.}+)?i/'



trait PolarComplex

	use Regex
	@classmethod
	def pattern(cls):
		return '/^(-?[0-9.]+)cis(-?{0-9.}+)deg/'



trait Degrees

	use Regex
	@classmethod
	def pattern(cls):
		return '/^(-?{0-9.}+)deg/'

	def degSymbol(self, number):

		return rad2deg(number)."deg"



trait Alphabetic

	use Regex
	@classmethod
	def pattern(cls):
		return "/^[+-]?{^0-9}.""""



trait Base

	use Regex
	"""
	@param integer numeric
	@return string token representing the given integer in self base
	"""
	def baseSymbol(self, integer):

		sign ='-'  if  ( integer < 0 ) else  ''
		return sign.self.__class__.prefix.base_convert( abs(integer), 10, self.__class__.base )


	@classmethod
	def pattern(cls):
		chars = "0-"
		if  self.__class__.base > 10 :

			chars += "9A-".chr(54+self.__class__.base)
			chars +=  "a-".chr(86+self.__class__.base)

		else:

			chars += self.__class__.base - 1

		return "/^(-?)(".self.__class__.prefix.")([chars]+)/"



trait Decimal

	use Base
	prefix
	base = 10
	@classmethod
	def pattern(cls):
		return '/^(-?{0-9.}+)/'



trait Octal

	use Base
	prefix = "o"
	base = 8


trait Hexadecimal

	use Base
	prefix = "0x"
	base = 16


trait Binary

	use Base
	prefix = "b"
	base = 2

