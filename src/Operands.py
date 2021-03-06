
import math
#namespace App.Operands

from Symbol import Operand
from Symbol import Operator
import Notations

def is_numeric(x):
	try:
		float(x)
		return True
	except:
		return False

class Scalar(Operand):

	"""
	@return the primitive scalar data
	"""
	def getValue(self):

		if isinstance(self.symbol, basestring):
			return float(self.symbol)
		return self.symbol


	"""
	@return string + or -
	"""
	def sign(self):

		return '+' if self.getValue() > 0 else '-'


	def operate(self, op, other = None):

		if isinstance(other, Complex):
			ret = op.scalarComplex( self, other )

		if  op.num_operands == 1 :
			ret = op.scalar( self )
		elif isinstance(other, Scalar):

			ret = op.scalar( self, other )

		if isinstance(other, Operand):
			return ret

		scalar = self.__class__(ret)
		scalar.setValue(ret)
		return scalar


	def bnot(self):

		return not self()

	def __str__(self):
		if float(self.symbol).is_integer():
			return str(int(self.symbol))
		return str(self.symbol)




class BaseScalar(Scalar):

	def getValue(self):

		( full, sign, prefix, value ) = self.__class__.regex( self.symbol )
		return (sign+base_convert( value, self.__class__.base, 10 )) * 1


	def setValue(self, value):

		self.symbol = self.baseSymbol( value )


	def bnot(self):

		base_width = len(self.symbol) - strlen(self.__class__.prefix)
		bin_width = ceil(log(self.__class__.base ** base_width, 2))
		mask = (( 1 << bin_width ) - 1)
		base_class = self.__class__.__name__
		negated = base_convert( not self() & mask, 10, self.__class__.base )
		symbol = self.__class__.prefix.str_pad( negated, base_width, '0', STR_PAD_LEFT)
		return base_class( symbol )


class DecScalar(Scalar, Notations.Decimal):
	pass
class OctScalar(BaseScalar, Notations.Octal):
	pass
class HexScalar(BaseScalar, Notations.Hexadecimal):
	pass
class BinScalar(BaseScalar, Notations.Binary):
	pass

class DegScalar(Scalar, Notations.Degrees):
	def getValue(self):

		raw_part = self.symbol.replace('deg',''); #substr( self.symbol, len(self.__class__.prefix) )
		return math.radians( raw_part )

	def setValue(self, value):

		self.symbol = self.degSymbol( value )




class Constant(Scalar, Notations.Alphabetic):
	def operate(self, op, other = None):

		doppelganger = DecScalar( self.getValue() )
		return doppelganger.operate(op, other)



class Pi    (Constant):
	def getValue(self):
		return M_PI
class Exp   (Constant):
	def getValue(self):
		return M_E
class Nan   (Constant):
	def getValue(self):
		return NAN
class PosInf(Constant):
	def getValue(self):
		return INF
class NegInf(Constant):
	def getValue(self):
		return -INF

class Complex(Operand, Notations.Complex):
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

		elif  isinstance( real, basestring ) :

			self.setValue( real )

		elif  is_numeric( real ) and is_numeric( imag ) :

			self.real = DecScalar( real )
			self.imag = DecScalar( imag )

		elif isinstance(real, Scalar) and isinstance( imag, Scalar ):

			self.real = real
			self.imag = imag



	"""
	@return  of the primitive real and imaginary values
	"""
	def getValue(self):

		return [ self.real(), self.imag() ]


	def setValue(self, string):

		matches = self.__class__.regex(string)
		#print matches
		real = matches[2] or 0
		imag =  ( matches[3] or '' ).replace('+','') + (matches[4] or 1)
		self.real = DecScalar( real * 1 )
		self.imag = DecScalar( imag * 1 )


	def __str__(self):

		if  self.real() == 0 :
			if  self.imag() == 1 :
				return "i"
			elif  self.imag() == -1 :
				return "-i"
			else:
				return str(self.imag)+"i"

	
		ret = str(self.real)
		if str(self.imag) == '1' :
			ret += "+i"
		elif str(self.imag) == '-1' :
			ret += "-i"
		elif  self.imag() != 0 :
			ret += ('+' if self.imag() >= 0 else '')+str(self.imag)+"i"
		return ret


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

		if  op.num_operands == 1 :

			if  op.implements('UnaryComplex') :

				ret = op.complex( self )


		elif isinstance(other, Complex):

			if  op.implements('BinaryComplex') :

				ret = op.complex( self, other )


		elif isinstance(other, Scalar):

			if  op.implements('BinaryComplexScalar') :

				ret = op.complexScalar( self, other )

		if   not  ret :
			return False

		if isinstance(ret, Operand):
			return ret

		return Complex( DecScalar(ret[0]), DecScalar(ret[1]) )


class PolarComplex(Complex, Notations.PolarComplex):
	def __init__(self, mag, arg=None):

		if  is_string( mag ) and arg is None :

			self.setValue(mag)

		else:

			self.setMagArg( mag, arg )



	def setValue(self, string):

		matches = self.__class__.regex(string)
		self.setMagArg( matches[1], math.radians(matches[2]) )


	def setMagArg(self, mag, arg):

		real = mag * cos( arg )
		imag = mag * sin( arg )
		if( abs(real) < 1e-10 ):real = 0
		if( abs(imag) < 1e-10 ):imag = 0
		self.real = DecScalar(real)
		self.imag = DecScalar(imag)


	def __str__(self):

		return self.mag()+"cis"+math.degrees(self.arg())+"deg"


