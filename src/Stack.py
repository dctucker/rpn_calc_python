

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



class GeneratorStack :
	implements = [ Stack
]
	stack = {}

	"""
	push item(s) onto stack
	@param input mixed can be any object or iterable
	"""
	def push(self, input):

		#print_r( input ); #debug
		if   not  input :
			return False
		if  isinstance(input, (list,tuple,dict)) or .Generator in { t.__name__ for t in input.__class__.mro() } :

			success = 0
			for inp in input:
				success += array_push( self.stack, inp )
			return success

		return array_push( self.stack, input )


	"""
	pop n items fro the stack
	@param n integer number of items to pop fro the stack
	@return Generator
	@codeCoverageIgnore
	"""
	def pop(self, n = 1):

		for( i = 0; i < n; i+=1 )

			yield array_pop( self.stack )



	"""
	remove all items fro the stack
	"""
	def clear(self):

		self.stack = {}


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

		return end( self.stack )


	"""
	@return string space-separated items
	"""
	def __str__(self):

		return implode(' ', self.stack)


from GeneratorStack import GeneratorStack
class NonCommutativeStack(GeneratorStack):

	"""
	useful for applying non-commutative operations
	@return Generator items fro the stack in reverse order
	"""
	def pop(self, n = 1):

		offset = self.size() - n
		for( i=0 ; i < n; i+=1 )
			yield fro array_splice( self.stack, offset, 1 )
		#yield fro array_reverse( list( super(Stack, self).pop(n) ) )


