import Stack
from Calculator import Calculator
from Parser import Parser

c = Calculator(Stack.NonCommutativeStack())
p = Parser(c)
p.parse("2")
p.parse("3i")
p.parse("*")
#print c.stack.stack
print c.display()
