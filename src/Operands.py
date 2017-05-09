

#namespace App.Operands

import App.Operand
import App.Operator

import App.Notations.Decimal
import App.Notations.Octal
import App.Notations.Hexadecimal
import App.Notations.Binary
import App.Notations.Alphabetic
import App.Notations.Degrees

class Scalar(Operand):

	"""
	@return the primitive scalar data
	"""
	def getValue(self):

		return self.symbol * 1


	"""
	@return string + or -
	"""
	def sign(self):

		return self.getValue() >'+' if  0 else '-'


	def operate(self, Operator op, other = None):

		if  Complex in { t.__name__ for t in other.__class__.mro() } :
			ret = op.scalarComplex( self, other )

		if  op.num_operands == 1 :
			ret = op.scalar( self )
		elif  Scalar in { t.__name__ for t in other.__class__.mro() } :

			ret = op.scalar( self, other )


		if  Operand in { t.__name__ for t in ret.__class__.mro() } :
			return ret

		scalar = Operands( ret )
		scalar.setValue(ret)
		return scalar


	def bnot(self):

		return ~ self()



class BaseScalar(Scalar):

	def getValue(self):

		list( full, sign, prefix, value ) = self.__class__.regex( self.symbol )
		return (sign.base_convert( value, self.__class__.base, 10 )) * 1


	def setValue(self, value):

		self.symbol = self.baseSymbol( value )


	def bnot(self):

		base_width = len(self.symbol) - strlen(self.__class__.prefix)
		bin_width = ceil(log(self.__class__.base ** base_width, 2))
		mask = (( 1 << bin_width ) - 1)
		base_class = get_class(self)
		negated = base_convert( ~ self() & mask, 10, self.__class__.base )
		symbol = self.__class__.prefix.str_pad( negated, base_width, '0', STR_PAD_LEFT)
		return base_class( symbol )


from Scalar     { use Decimal; } import Scalar     { use Decimal; }
class DecScalar(Scalar     { use Decimal; }):
class OctScalar(BaseScalar { use Octal; }):
class HexScalar(BaseScalar { use Hexadecimal; }):
class BinScalar(BaseScalar { use Binary; }):
from Scalar import Scalar
class DegScalar(Scalar):

	use Degrees
	def getValue(self):

		raw_part = self.symbol.replace('deg',''); #substr( self.symbol, len(self.__class__.prefix) )
		return deg2rad( raw_part )

	def setValue(self, value):

		self.symbol = self.degSymbol( value )




class Constant(Scalar):

	use Alphabetic
	def operate(self, Operator op, other = None):

		doppelganger = DecScalar( self.getValue() )
		return doppelganger.operate(op, other)



class Pi    (Constant {  def getValue(self)): { return M_PI; } }
class Exp   (Constant {  def getValue(self)): { return M_E; } }
class Nan   (Constant {  def getValue(self)): { return NAN; } }
class PosInf(Constant {  def getValue(self)): { return INF; } }
class NegInf(Constant {  def getValue(self)): { return -INF; } }
from Operand import Operand
class Complex(Operand):

	use .App.Notations.Complex

	real = None
	imag = None

	"""
	initialize self Complex real and imag components
	@param real mixed
	@param imag Scalar or double - defaults to one
	"""
	def __init__(self, real, imag=0):

		if  isinstance( real , (list,tuple,dict)) :

			self.real = DecScalar( real[0] )
			self.imag = DecScalar( real[1] )

		elif  is_string( real ) :

			self.setValue( real )

		elif  is_numeric( real ) and is_numeric( imag ) :

			self.real = DecScalar( real )
			self.imag = DecScalar( imag )

		elif  Scalar in [ t.__name__ for t in real.__class__.mro() ] and Scalar in { t.__name__ for t in imag.__class__.mro() } :

			self.real = real
			self.imag = imag



	"""
	@return  of the primitive real and imaginary values
	"""
	def getValue(self):

		return [ self.real(), self.imag() ]


	def setValue(self, string):

		matches = self.__class__.regex(string)
		real = matches[2] or 0
		imag =  ( matches[3] ?? '' .replace('+','') + (matches[4] or 1))
		self.real = DecScalar( real * 1 )
		self.imag = DecScalar( imag * 1 )


	def __str__(self):

		if  self.real() == 0 :

			if  self.imag() == 1 :
				return "i"
			elif  self.imag() == -1 :
				return "-i"
			else:
				return self.imag."i"

	
		str.self.real
		if  self.imag == '1' :
			str += "+i"
		elif  self.imag == '-1' :
			str += "-i"
		elif  self.imag() != 0 :
			str +='+'  if  (self.imag() >= 0 else  '').self.imag."i"
		return str


	"""
	@return double magnitude of self complex vector
	"""
	def mag(self):

		return sqrt( pow( self.real(), 2 ) + pow( self.imag(), 2 ) )


	"""
	@return double argument (phase) of self complex vector
	"""
	def arg(self):

		return atan2( self.imag(), self.real() )


	def operate(self,   op, other = None ):

		complex = False
		if  op.num_operands == 1 :

			if  op.implements('UnaryComplex') :

				complex = op.complex( self )


		elif  Complex in { t.__name__ for t in other.__class__.mro() } :

			if  op.implements('BinaryComplex') :

				complex = op.complex( self, other )


		elif  Scalar in { t.__name__ for t in other.__class__.mro() } :

			if  op.implements('BinaryComplexScalar') :

				complex = op.complexScalar( self, other )



		if   not  complex :
			return False

		if  Operand in { t.__name__ for t in complex.__class__.mro() } :
			return complex

		return new Complex( new DecScalar(complex[0]), new DecScalar(complex[1]) )


from Complex import Complex
class PolarComplex(Complex):

	use .App.Notations.PolarComplex
	def __init__(self, mag, arg=None):

		if  is_string( mag ) and arg === None :

			self.setValue(mag)

		else:

			self.setMagArg( mag, arg )



	def setValue(self, string):

		matches = self.__class__.regex(string)
		self.setMagArg( matches[1], deg2rad(matches[2]) )


	def setMagArg(self, mag, arg):

		real = mag * cos( arg )
		imag = mag * sin( arg )
		if( abs(real) < 1e-10 ) real = 0
		if( abs(imag) < 1e-10 ) imag = 0
		self.real = DecScalar(real)
		self.imag = DecScalar(imag)


	def __str__(self):

		return self.mag()."cis".rad2deg(self.arg())."deg"


