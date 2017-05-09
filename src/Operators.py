

#namespace App.Operators

from Factory import OperatorFactory
from Symbol import Operator
from Factory import OperandFactory
from Symbol import Operand
from Operands import Scalar
from Operands import BaseScalar
from Operands import Complex
from Operands import PolarComplex
from Notations import Base
from Notations import Degrees
from Notations import Binary
from Notations import Octal
from Notations import Decimal
from Notations import Hexadecimal



class StackOperator  :
	pass
class ComplexOperator:
	pass
class ScalarOperator :
	pass
class UnaryScalar   ( ScalarOperator  ):
	def scalar(self, s):
		pass
class BinaryScalar  ( ScalarOperator  ):
	def scalar(self, s1,  s2):
		pass
class UnaryComplex  ( ComplexOperator ):
	def complex(self, c):
		pass
class BinaryComplex ( ComplexOperator ):
	def complex(self, c1,  c2):
		pass
class BinaryComplexScalar (ComplexOperator):

	def scalarComplex(self, c,  s):
		pass

	def complexScalar(self, c,  s):
		pass



class UnaryOperator(Operator, UnaryScalar):
	num_operands = 1

	"""
	take a single operand and apply operator to it
	@param operands iterable of operand(s) - only first is used
	@return Operand
	"""
	def __call__(self, *operands):

		operands = self.generate( operands )
		
		ret = operands.current()
		if  operands.valid() :
			ret = ret.operate( self )
		return ret



class BinaryOperator(Operator, BinaryScalar ):
	num_operands = 2

	"""
	take operands and apply operator to them in sequence
	@param operands iterable of operands
	@return Operand
	"""
	def __call__(self, *operands):

		operands = self.generate( operands )

		for operand in operands:
			ret = operand
			break
		for operand in operands:
			ret = ret.operate( self, operand )
		return ret



# stack operations
class Pop(Operator, StackOperator):
	num_operands = 1
	"""
	incoming operand(s) will the raisen away.
	@param operand Generator of items to discard
	@return void
	"""
	def __call__(self, *operand):

		pass # NOP


class Push(Operator, StackOperator):
	num_operands = 1
	"""
	incoming operand will duplicated.
	@param operand mixed item to duplicate
	@return Generator
	@codeCoverageIgnore
	"""
	def __call__(self, *operands):

		operands = self.generate(operands)
		operand = operands.current()
		if  operand :

			yield operand
			yield operand



class Swap(Operator, StackOperator):
	num_operands = 2
	"""
	@param @operands Generator of items
	@return Generator of items in reverse order
	"""
	def __call__(self, *operands):

		operands = self.generate( operands )
		for o in operands.reverse():
			yield o




# arithmetic operations

class AddComplex:

	def complex(self, c1,  c2):

		return [
			self.scalar( c1.real, c2.real ),
			self.scalar( c1.imag, c2.imag )
		]


class Plus(BinaryOperator, BinaryComplex, BinaryComplexScalar, AddComplex):
	def scalar(self, s1,  s2):

		return s1() + s2()

	def complexScalar(self, c,  s):

		return {
			c.real() + s(),
			c.imag(),
		}

	def scalarComplex(self, s,  c):

		return Complex([
			s() + c.real(),
			c.imag(),
		])

class Minus(BinaryOperator, BinaryComplex, BinaryComplexScalar, AddComplex):
	def scalar(self, s1,  s2):

		return s1() - s2()

	def complexScalar(self, c,  s):

		return {
			c.real() - s(),
			c.imag(),
		}

	def scalarComplex(self, s,  c):

		return Complex([
			s() - c.real(),
			- c.imag(),
		])


class Times(BinaryOperator, BinaryComplex, BinaryComplexScalar):
	def scalar(self, s1,  s2):

		return s1() * s2()

	def complex(self, c1,  c2):

		ac = c1.real() * c2.real()
		bd = c1.imag() * c2.imag()
		ad = c1.real() * c2.imag()
		bc = c1.imag() * c2.real()
		return {
			ac - bd ,
			ad + bc ,
		}

	"""
	multiply both components of the given Complex by the given Scalar
	@return data for constructing a Complex
	"""
	def complexScalar(self, c,  s):

		return {
			self.scalar( s, c.real ),
			self.scalar( s, c.imag )
		}

	def scalarComplex(self, s,  c):

		return Complex( self.complexScalar(c, s) ) # commutative

class Divide(BinaryOperator, BinaryComplex, BinaryComplexScalar):
	def __init__(self, symbol):

		super(Operators, self).__init__(symbol)
		self.times = OperatorFactory.make('*')
		self.recip = OperatorFactory.make('1/x')

	def scalar(self, s1,  s2):

		if  s2() == 0 :
			return NAN
		return self.times.scalar( s1, self.recip( s2 ) )


	def complex(self, c1,  c2):

		ac = c1.real() * c2.real()
		bc = c1.imag() * c2.real()
		ad = c1.real() * c2.imag()
		bd = c1.imag() * c2.imag()
		cc = c2.real(); cc *= cc
		dd = c2.imag(); dd *= dd
		if  cc + dd == 0 :
			return [NAN,NAN]
		return {
			(ac + bd) / ( cc + dd ),
			(bc - ad) / ( cc + dd )
		}


	def scalarComplex(self, s,  c):

		return  self.times.scalarComplex( s, c.operate(self.recip) )


	def complexScalar(self, c,  s):

		return self.times.complexScalar( c, self.recip( s ) )


class Reciprocal(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		if  s() == 0 :
			return NAN
		return 1 / s()

	def complex(self, c):

		xx = c.real(); xx *= xx
		yy = c.imag(); yy *= yy
		if  xx + yy == 0 :
			return [NAN,NAN]
		return [
			 c.real() / ( xx + yy ),
			- c.imag() / ( xx + yy )
		]


class Negative(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return - s()

	def complex(self, c):

		return {
			- c.real(),
			- c.imag()
		}


class Modulo(BinaryOperator):

	def scalar(self, s1,  s2):

		if  s2() == 0 :
			return NAN
		return fmod( s1(), s2() )



class Intval(UnaryOperator):

	def scalar(self, s1):

		return int(s1())



class Frac(UnaryOperator):

	def scalar(self, s):

		return s() - floor(s())



class Round(UnaryOperator):

	def scalar(self, s):

		return round(s())




# base conversion operations

class BaseOperator(UnaryOperator, Base):

	def scalar(self, s):

		string = self.baseSymbol( s() )
		return OperandFactory.make( string )


class Bin(BaseOperator, Binary): pass
class Oct(BaseOperator, Octal): pass
class Dec(BaseOperator, Decimal): pass
class Hex(BaseOperator, Hexadecimal): pass

class Dump(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		var_dump(s)
		return s

	def complex(self, c):

		var_dump(c)
		return c



# bitwise operations
class BAnd(BinaryOperator):

	def scalar(self, s1,  s2):

		return s1() & s2()


class BOr(BinaryOperator):

	def scalar(self, s1,  s2):

		return s1() | s2()


class BXor(BinaryOperator):

	def scalar(self, s1,  s2):

		return s1() ^ s2()



class BNot(UnaryOperator):

	def scalar(self, s):

		return s.bnot()


class BShiftLeft(BinaryOperator):

	def scalar(self, s1,  s2):

		return s1() << s2()


class BShiftRight(BinaryOperator):

	def scalar(self, s1,  s2):

		return s1() >> s2()



# exponentation operations
class Power(BinaryOperator, BinaryComplex, BinaryComplexScalar):
	def scalar(self, s1,  s2):

		return s1() ** s2(); # y^x, not x^y

	def complex(self, c1,  c2):

 		aabb = c1.real() ** 2 + c1.imag() ** 2
		mag = aabb ** (c2.real() / 2) * exp( -c2.imag() * c1.arg() )
		arg = c2.real() * c1.arg() + 0.5 * c2.imag() * log( aabb )
		return PolarComplex(mag, arg)

	def complexScalar(self, c,  s):

		return self.complex( c, Complex( s, OperandFactory.make('0') ) )

	def scalarComplex(self, s,  c):

		return self.complex( OperandFactory.make(s()+'+0i'), c )


class Sqrt(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		if  s() < 0 :
			return Complex(
				0,
				sqrt( abs( s() ) )
			)
		return sqrt( s() )


	def complex(self, c):

		aa = c.real(); aa *= aa
		bb = c.imag(); bb *= bb
		sq = sqrt( aa + bb )
		sign = c.imag() < 0
		return [
			sqrt( (   c.real() + sq ) / 2 ),
			sqrt( ( - c.real() + sq ) / 2 ) * sign
		]



class Ln(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return log( s() )

	def complex(self, c):

		return [
			log( c.mag() ),
			c.arg()
		]


class NthLog(BinaryOperator, BinaryComplexScalar):
	def scalar(self, s1,  s2):

		return log( s1(), s2() )

	def complexScalar(self, c,  s):

		return {
			log( c.mag() ) / log( s() ),
			c.arg() / log( s() )
		}

	def scalarComplex(self, s,  c):

		div = OperatorFactory.make('/')
		ln = OperatorFactory.make('ln')
		return div( s.operate(ln), c.operate(ln) )



# trigonometric operations

class TrigOperator(UnaryOperator):
	pass

class Sin(TrigOperator, UnaryComplex):
	def scalar(self, s):

		return sin( s() )


	def complex(self, c):

		return [
			sin( c.real() ) * cosh( c.imag() ),
			cos( c.real() ) * sinh( c.imag() )
		]

class Cos(TrigOperator, UnaryComplex):
	def scalar(self, s):

		return cos( s() )

	def complex(self, c):

		return [
			 cos( c.real() ) * cosh( c.imag() ),
			- sin( c.real() ) * sinh( c.imag() )
		]

class Tan(TrigOperator, UnaryComplex):
	def __init__(self, symbol):

		super(Operators, self).__init__(symbol)
		self.cos = OperatorFactory.make('cos')
		self.sin = OperatorFactory.make('sin')
		self.div = OperatorFactory.make('/')

	def scalar(self, s):

		return tan( s() )

	def complex(self, c):

		return self.div( self.sin(c) , self.cos(c) )


class Degree(TrigOperator, Degrees):

	def scalar(self, s):

		return OperandFactory.make( self.degSymbol( s() ) )


class Radian(TrigOperator):

	def scalar(self, s):

		return OperandFactory.make(s())



# complex-oriented operations

class Mag(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return abs( s() )

	def complex(self, c):

		return OperandFactory.make(c.mag())



class Arg(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return atan2( 0, s() )

	def complex(self, c):

		return OperandFactory.make(c.arg())



class Conj(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return s()

	def complex(self, c):

		return [
			 c.real(),
			- c.imag()
		]



class RealPart(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return s()

	def complex(self, c):

		return c.real



class ImagPart(UnaryOperator, UnaryComplex):
	def scalar(self, s):

		return 0

	def complex(self, c):

		return c.imag


