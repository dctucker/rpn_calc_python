import Stack
from Calculator import Calculator
from Parser import Parser

c = Calculator(Stack.NonCommutativeStack())
p = Parser(c)
p.parse("2")
print c.display()
p.parse("1")
print c.display()
p.parse("/")
print c.display()
#print c.stack.stack
