
import types
#namespace App

class Stack:

	def push(self, input):
		pass

	def pop(self, n):
		pass

	def size(self):
		pass

	def all(self):
		pass

	def peek(self):
		pass

	def __str__(self):
		pass



class GeneratorStack(Stack):
	stack = []

	"""
	push item(s) onto stack
	@param input mixed can be any object or iterable
	"""
	def push(self, input):

		#print_r( input ); #debug
		if   not  input :
			return False
		if  isinstance(input, (list,tuple,dict)) or isinstance(input, types.GeneratorType):

			success = 0
			for inp in input:
				self.stack.append( input )
			return success

		return self.stack.append( input )


	"""
	pop n items fro the stack
	@param n integer number of items to pop fro the stack
	@return Generator
	@codeCoverageIgnore
	"""
	def pop(self, n = 1):

		i = 0
		while i < n:

			yield self.stack.pop()
			i += 1



	"""
	remove all items fro the stack
	"""
	def clear(self):

		self.stack = []


	"""
	@return integer number of items on the stack
	"""
	def size(self):

		return len( self.stack )


	"""
	@return all items on the stack
	"""
	def all(self):

		return self.stack


	"""
	@return the item on the top of the stack
	"""
	def peek(self):

		return self.stack[-1]


	"""
	@return string space-separated items
	"""
	def __str__(self):

		return ' '.join([ str(s) for s in self.stack])


class NonCommutativeStack(GeneratorStack):

	"""
	useful for applying non-commutative operations
	@return Generator items fro the stack in reverse order
	"""
	def pop(self, n = 1):

		offset = self.size() - n
		i = 0
		while i < n:
			removed = self.stack[offset]
			del self.stack[offset]
			yield removed
			i += 1
		#yield fro array_reverse( list( super(Stack, self).pop(n) ) )


