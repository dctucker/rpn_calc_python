

#namespace App

import App.Operand
import App.Operator

class Calculator:

	warning = False
	previous_stack = None

	def __init__(self, Stack stack):

		self.stack = stack


	"""
	enter a symbol into the calculator
	push onto stack or apply the given operator
	"""
	def push(self, Symbol sym):

		self.warning = False
		if  Operator in { t.__name__ for t in sym.__class__.mro() } :
			return self.applyOperator( sym )
		elif  Operand in { t.__name__ for t in sym.__class__.mro() } :
			return self.stack.push( sym )


	"""
	pop the stack and apply the operator, issue warnings if needed
	@return integer or boolean, False if unsuccessful
	"""
	def applyOperator(self, Operator operator):

		self.backup()

		stacksize = self.stack.size()
		missing = operator.num_operands - stacksize
		if  missing > 0 :

			self.warning = "Operator operator requires " + missing + " more on stack."
			return False

		operands = self.stack.pop( operator.num_operands )
		result = operator( *operands )
		if  result === False :

			self.restore()
			required_interface = operator.getRequiredInterface()
			self.warning = "Operator 'operator' not supported for the given operands (" + required_interface + ")"
			return False

		return self.stack.push( result )


	"""
	@return string the item on the top of the stack
	"""
	def display(self):

		return "".self.stack


	"""
	remember the state of the current stack
	"""
	def backup(self):

		self.previous_stack = clone self.stack


	"""
	reset the stack to its previously backed-up state
	"""
	def restore(self):

		self.stack = self.previous_stack


