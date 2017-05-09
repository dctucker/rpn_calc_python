

#namespace App.Operators

import App.OperatorFactory
import App.Operator
import App.OperandFactory
import App.Operand
import App.Operands.Scalar
import App.Operands.BaseScalar
import App.Operands.Complex
import App.Operands.PolarComplex
import App.Notations.Degrees
import App.Notations.Binary
import App.Notations.Octal
import App.Notations.Decimal
import App.Notations.Hexadecimal



class StackOperator  :
	pass
class ComplexOperator:
	pass
class ScalarOperator :
	pass
interface UnaryScalar   extends ScalarOperator  {  def scalar(self, Scalar s):; }
interface BinaryScalar  extends ScalarOperator  {  def scalar(self, Scalar s1,  s2):; }
interface UnaryComplex  extends ComplexOperator {  def complex(self, Complex c):; }
interface BinaryComplex extends ComplexOperator {  def complex(self, Complex c1,  c2):; }
class BinaryComplexScalar (ComplexOperator):

	def scalarComplex(self, Scalar c,  s):
		pass

	def complexScalar(self, Complex c,  s):
		pass



class UnaryOperator(Operator ):
	implements = [ UnaryScalar
]
	num_operands = 1

	"""
	take a single operand and apply operator to it
	@param operands iterable of operand(s) - only first is used
	@return Operand
	"""
	def __invoke(self, *operands):

		operands = self.generate( operands )
		
		ret = operands.current()
		if  operands.valid() :
			ret = ret.operate( self )
		return ret



class BinaryOperator(Operator ):
	implements = [ BinaryScalar
]
	num_operands = 2

	"""
	take operands and apply operator to them in sequence
	@param operands iterable of operands
	@return Operand
	"""
	def __invoke(self, *operands):

		operands = self.generate( operands )

		ret = operands.current()
		for( operands.next(); operands.valid(); operands.next() )
			ret = ret.operate( self, operands.current() )
		return ret



# stack operations
from Operator  import Operator 
class Pop(Operator ):
	implements = [ StackOperator
]
	num_operands = 1
	"""
	incoming operand(s) will the raisen away.
	@param operand Generator of items to discard
	@return void
	"""
	def __invoke(self, *operand):

		# NOP


from Operator  import Operator 
class Push(Operator ):
	implements = [ StackOperator
]
	num_operands = 1
	"""
	incoming operand will duplicated.
	@param operand mixed item to duplicate
	@return Generator
	@codeCoverageIgnore
	"""
	def __invoke(self, *operands):

		operands = self.generate(operands)
		operand = operands.current()
		if  operand :

			yield operand
			yield operand



from Operator  import Operator 
class Swap(Operator ):
	implements = [ StackOperator
]
	num_operands = 2
	"""
	@param @operands Generator of items
	@return Generator of items in reverse order
	"""
	def __invoke(self, *operands):

		operands = self.generate( operands )
		yield fro array_reverse( list( operands ) )




# arithmetic operations

trait AddComplex

	def complex(self, Complex c1,  c2):

		return {
			self.scalar( c1.real, c2.real ),
			self.scalar( c1.imag, c2.imag )
		}


from BinaryOperator  import BinaryOperator 
class Plus(BinaryOperator ):
	implements = [ BinaryComplex, BinaryComplexScalar
]
	use AddComplex
	def scalar(self, Scalar s1,  s2):

		return s1() + s2()

	def complexScalar(self, Complex c,  s):

		return {
			c.real() + s(),
			c.imag(),
		}

	def scalarComplex(self, Scalar s,  c):

		return new Complex({
			s() + c.real(),
			c.imag(),
		})

from BinaryOperator  import BinaryOperator 
class Minus(BinaryOperator ):
	implements = [ BinaryComplex, BinaryComplexScalar
]
	use AddComplex
	def scalar(self, Scalar s1,  s2):

		return s1() - s2()

	def complexScalar(self, Complex c,  s):

		return {
			c.real() - s(),
			c.imag(),
		}

	def scalarComplex(self, Scalar s,  c):

		return new Complex({
			s() - c.real(),
			- c.imag(),
		})


from BinaryOperator  import BinaryOperator 
class Times(BinaryOperator ):
	implements = [ BinaryComplex, BinaryComplexScalar
]
	def scalar(self, Scalar s1,  s2):

		return s1() * s2()

	def complex(self, Complex c1,  c2):

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
	def complexScalar(self, Complex c,  s):

		return {
			self.scalar( s, c.real ),
			self.scalar( s, c.imag )
		}

	def scalarComplex(self, Scalar s,  c):

		return new Complex( self.complexScalar(c, s) ); # commutative

from BinaryOperator  import BinaryOperator 
class Divide(BinaryOperator ):
	implements = [ BinaryComplex, BinaryComplexScalar
]
	def __init__(self, symbol):

		super(Operators, self).__init__(symbol)
		self.times = OperatorFactory.make('*')
		self.recip = OperatorFactory.make('1/x')

	def scalar(self, Scalar s1,  s2):

		if  s2() == 0 :
			return NAN
		return self.times.scalar( s1, self.recip( s2 ) )


	def complex(self, Complex c1,  c2):

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


	def scalarComplex(self, Scalar s,  c):

		return  self.times.scalarComplex( s, c.operate(self.recip) )


	def complexScalar(self, Complex c,  s):

		return self.times.complexScalar( c, self.recip( s ) )

from UnaryOperator  import UnaryOperator 
class Reciprocal(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		if  s() == 0 :
			return NAN
		return 1 / s()

	def complex(self, Complex c):

		xx = c.real(); xx *= xx
		yy = c.imag(); yy *= yy
		if  xx + yy == 0 :
			return [NAN,NAN]
		return {
			 c.real() / ( xx + yy ),
			- c.imag() / ( xx + yy )
		}

from UnaryOperator  import UnaryOperator 
class Negative(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return - s()

	def complex(self, Complex c):

		return {
			- c.real(),
			- c.imag()
		}


from BinaryOperator import BinaryOperator
class Modulo(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		if  s2() == 0 :
			return NAN
		return fmod( s1(), s2() )


from UnaryOperator import UnaryOperator
class Intval(UnaryOperator):

	def scalar(self, Scalar s1):

		return int(s1())


from UnaryOperator import UnaryOperator
class Frac(UnaryOperator):

	def scalar(self, Scalar s):

		return s() - floor(s())


from UnaryOperator import UnaryOperator
class Round(UnaryOperator):

	def scalar(self, Scalar s):

		return round(s())




# base conversion operations

class BaseOperator(UnaryOperator):

	use .App.Notations.Base
	def scalar(self, Scalar s):

		string = self.baseSymbol( s() )
		return OperandFactory.make( string )


from BaseOperator { use Binary; } import BaseOperator { use Binary; }
class Bin(BaseOperator { use Binary; }):
class Oct(BaseOperator { use Octal; }):
class Dec(BaseOperator { use Decimal; }):
class Hex(BaseOperator { use Hexadecimal; }):
from UnaryOperator  import UnaryOperator 
class Dump(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		var_dump(s)
		return s

	def complex(self, Complex c):

		var_dump(c)
		return c



# bitwise operations
from BinaryOperator import BinaryOperator
class BAnd(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		return s1() & s2()


from BinaryOperator import BinaryOperator
class BOr(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		return s1() | s2()


from BinaryOperator import BinaryOperator
class BXor(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		return s1() ^ s2()


from UnaryOperator import UnaryOperator
class BNot(UnaryOperator):

	def scalar(self, Scalar s):

		return s.bnot()


from BinaryOperator import BinaryOperator
class BShiftLeft(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		return s1() << s2()


from BinaryOperator import BinaryOperator
class BShiftRight(BinaryOperator):

	def scalar(self, Scalar s1,  s2):

		return s1() >> s2()



# exponentation operations
from BinaryOperator  import BinaryOperator 
class Power(BinaryOperator ):
	implements = [ BinaryComplex, BinaryComplexScalar
]
	def scalar(self, Scalar s1,  s2):

		return s1() ** s2(); # y^x, not x^y

	def complex(self, Complex c1,  c2):

 		aabb = c1.real() ** 2 + c1.imag() ** 2
		mag = aabb ** (c2.real() / 2) * exp( -c2.imag() * c1.arg() )
		arg = c2.real() * c1.arg() + 0.5 * c2.imag() * log( aabb )
		return PolarComplex(mag, arg)

	def complexScalar(self, Complex c,  s):

		return self.complex( c, new Complex( s, OperandFactory.make('0') ) )

	def scalarComplex(self, Scalar s,  c):

		return self.complex( OperandFactory.make(s().'+0i'), c )

from UnaryOperator  import UnaryOperator 
class Sqrt(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		if  s() < 0 :
			return new Complex(
				0,
				sqrt( abs( s() ) )
			)
		return sqrt( s() )


	def complex(self, Complex c):

		aa = c.real(); aa *= aa
		bb = c.imag(); bb *= bb
		sq = sqrt( aa + bb )
		sign = c.imag() <: 0
		return {
			sqrt( (   c.real() + sq ) / 2 ),
			sqrt( ( - c.real() + sq ) / 2 ) * sign
		}


from UnaryOperator  import UnaryOperator 
class Ln(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return log( s() )

	def complex(self, Complex c):

		return {
			log( c.mag() ),
			c.arg()
		}


from BinaryOperator  import BinaryOperator 
class NthLog(BinaryOperator ):
	implements = [ BinaryComplexScalar
]
	def scalar(self, Scalar s1,  s2):

		return log( s1(), s2() )

	def complexScalar(self, Complex c,  s):

		return {
			log( c.mag() ) / log( s() ),
			c.arg() / log( s() )
		}

	def scalarComplex(self, Scalar s,  c):

		div = OperatorFactory.make('/')
		ln = OperatorFactory.make('ln')
		return div( s.operate(ln), c.operate(ln) )



# trigonometric operations

class TrigOperator(UnaryOperator):


from TrigOperator  import TrigOperator 
class Sin(TrigOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return sin( s() )


	def complex(self, Complex c):

		return {
			sin( c.real() ) * cosh( c.imag() ),
			cos( c.real() ) * sinh( c.imag() )
		}

from TrigOperator  import TrigOperator 
class Cos(TrigOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return cos( s() )

	def complex(self, Complex c):

		return {
			 cos( c.real() ) * cosh( c.imag() ),
			- sin( c.real() ) * sinh( c.imag() )
		}

from TrigOperator  import TrigOperator 
class Tan(TrigOperator ):
	implements = [ UnaryComplex
]
	def __init__(self, symbol):

		super(Operators, self).__init__(symbol)
		self.cos = OperatorFactory.make('cos')
		self.sin = OperatorFactory.make('sin')
		self.div = OperatorFactory.make('/')

	def scalar(self, Scalar s):

		return tan( s() )

	def complex(self, Complex c):

		return self.div( self.sin(c) , self.cos(c) )


from TrigOperator import TrigOperator
class Degree(TrigOperator):

	use Degrees
	def scalar(self, Scalar s):

		return OperandFactory.make( self.degSymbol( s() ) )


from TrigOperator import TrigOperator
class Radian(TrigOperator):

	def scalar(self, Scalar s):

		return OperandFactory.make(s())



# complex-oriented operations
from UnaryOperator  import UnaryOperator 
class Mag(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return abs( s() )

	def complex(self, Complex c):

		return OperandFactory.make(c.mag())


from UnaryOperator  import UnaryOperator 
class Arg(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return atan2( 0, s() )

	def complex(self, Complex c):

		return OperandFactory.make(c.arg())


from UnaryOperator  import UnaryOperator 
class Conj(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return s()

	def complex(self, Complex c):

		return {
			 c.real(),
			- c.imag()
		}


from UnaryOperator  import UnaryOperator 
class RealPart(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return s()

	def complex(self, Complex c):

		return c.real


from UnaryOperator  import UnaryOperator 
class ImagPart(UnaryOperator ):
	implements = [ UnaryComplex
]
	def scalar(self, Scalar s):

		return 0

	def complex(self, Complex c):

		return c.imag


