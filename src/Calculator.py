
import copy
#namespace App

from Symbol import Operand
from Symbol import Operator

class Calculator:

	warning = False
	previous_stack = None

	def __init__(self, stack):

		self.stack = stack


	"""
	enter a symbol into the calculator
	push onto stack or apply the given operator
	"""
	def push(self, sym):

		self.warning = False
		if isinstance(sym,Operator):
			return self.applyOperator( sym )
		elif isinstance(sym,Operand):
			return self.stack.push( sym )


	"""
	pop the stack and apply the operator, issue warnings if needed
	@return integer or boolean, False if unsuccessful
	"""
	def applyOperator(self, operator):

		self.backup()

		stacksize = self.stack.size()
		missing = operator.num_operands - stacksize
		if  missing > 0 :

			self.warning = "Operator operator requires " + missing + " more on stack."
			return False

		operands = self.stack.pop( operator.num_operands )
		result = operator( *operands )
		if  result is False :

			self.restore()
			required_interface = operator.getRequiredInterface()
			self.warning = "Operator 'operator' not supported for the given operands (" + required_interface + ")"
			return False

		return self.stack.push( result )


	"""
	@return string the item on the top of the stack
	"""
	def display(self):

		return str(self.stack)


	"""
	remember the state of the current stack
	"""
	def backup(self):

		self.previous_stack = copy.copy( self.stack )


	"""
	reset the stack to its previously backed-up state
	"""
	def restore(self):

		self.stack = self.previous_stack


