import sys
import time
from datetime import timedelta

class VirtualMachine:
	def __init__(self):
		self.quads             = []
		self.iterators         = []
		self.global_memory     = dict()
		self.function_memory   = [dict()]
		self.activation_record = []
		self.start_time        = 0
		self.end_time          = 0
		self.funcs             = {
			"="       : self.equals,
			"*"       : self.multiplication,
			"/"       : self.division,
			"+"       : self.plus,
			"-"       : self.minus,
			"<"       : self.less_than,
			">"       : self.greater_than,
			"<="      : self.less_equal,
			">="      : self.greater_equal,
			"!="      : self.different,
			"=="      : self.same,
			"&&"      : self.compare_and,
			"||"      : self.compare_or,
			"PRINT"   : self.print,
			"INPUT"   : self.input,
			"GOTO"    : self.goto,
			"GOTOF"   : self.gotof,
			"ERA"     : self.era, 
			"PARAM"   : self.param,
			"GOSUB"   : self.gosub,
			"RETURN"  : self.return_value,
			"ENDPROC" : self.end_proc,
			"VER"     : self.ver,
			"END"     : self.end
		}

	def execute(self):
		print("executing...")
		self.start_time = time.monotonic()
		self.iterators.append(0)

		while True:
			clean_quad = self.clean_quad(self.quads[self.iterators[-1]])
			#print(clean_quad)
			self.funcs[clean_quad[0]](clean_quad)
			self.iterators[-1] = self.iterators[-1] + 1

	def clean_quad(self, quad):
		

		if not quad[1] is None and quad[1].__class__.__name__ in ('tuple'):
			new_quad = quad[:1]+(self.clean_tuple(quad[1],1),)+quad[2:4]
			quad = new_quad

		if not quad[2] is None and quad[2].__class__.__name__ in ('tuple'):
			new_quad = quad[:2]+(self.clean_tuple(quad[2],2),)+quad[3:4]
			quad = new_quad

		if not quad[3] is None and quad[3].__class__.__name__ in ('tuple'):
			new_quad = quad[:3]+(self.clean_tuple(quad[3],3),)
			quad = new_quad

		return quad

	def clean_tuple(self, tp, n):
		if tp[0] == "cte":
			if n == 1:
				self.global_memory[50000] = tp[1]
				return 50000
			elif n == 2:
				self.global_memory[50001] = tp[1]
				return 50001
			else:
				self.global_memory[50002] = tp[1]
				return 50002
		else:
			#pointer
			return self.value_from_memory(tp[1]) # memory[tp[1]]

	def value_from_memory(self, address):
		if address < 20000 or address >= 50000:
			#global memory
			if address in self.global_memory:
				return self.global_memory[address]
			else:
				print("Error, used variable before initalization")
				sys.exit(0)
		else:
			if address in self.function_memory[-1]:
				return self.function_memory[-1][address]
			else:
				print("Error, used variable before initalization")
				sys.exit(0)

	def value_from_memory_below(self, address):
		if address < 20000 or address >= 50000:
			#global memory
			if address in self.global_memory:
				return self.global_memory[address]
			else:
				print("Error, used variable before initalization")
				sys.exit(0)
		else:
			if address in self.function_memory[-2]:
				return self.function_memory[-2][address]
			else:
				print("Error, used variable before initalization")
				sys.exit(0)

	def value_to_memory(self, address, value):
		if address < 20000 or address >= 50000:
			self.global_memory[address] = value
		else:
			self.function_memory[-1][address] = value
		

	def equals(self, quad):
		self.value_to_memory(quad[3], self.value_from_memory(quad[1]))

	def multiplication(self, quad):
		temp = self.value_from_memory(quad[1]) * self.value_from_memory(quad[2])
		self.value_to_memory(quad[3], temp)

	def division(self, quad):
		temp = self.value_from_memory(quad[1]) / self.value_from_memory(quad[2])
		self.value_to_memory(quad[3], temp)

	def plus(self, quad):
		temp = self.value_from_memory(quad[1]) + self.value_from_memory(quad[2])
		self.value_to_memory(quad[3], temp)

	def minus(self, quad):
		temp = self.value_from_memory(quad[1]) - self.value_from_memory(quad[2])
		self.value_to_memory(quad[3], temp)

	def less_than(self, quad):
		if self.value_from_memory(quad[1]) < self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def greater_than(self, quad):
		if self.value_from_memory(quad[1]) > self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def less_equal(self, quad):
		if self.value_from_memory(quad[1]) <= self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def greater_equal(self, quad):
		if self.value_from_memory(quad[1]) >= self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def different(self, quad):
		if self.value_from_memory(quad[1]) != self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def same(self, quad):
		if self.value_from_memory(quad[1]) == self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def compare_and(self, quad):
		if self.value_from_memory(quad[1]) and self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def compare_or(self, quad):
		if self.value_from_memory(quad[1]) or self.value_from_memory(quad[2]):
			self.value_to_memory(quad[3], True)
		else:
			self.value_to_memory(quad[3], False)

	def print(self, quad):
		if isinstance(quad[1], str):
			print(quad[1])
		else:
			print(self.value_from_memory(quad[1]))

	#solamente checa que sea int
	def input(self, quad):
		#checar el tipo de la entrada
		user_input = input()

		if quad[1] == "Bool":

			if user_input.lower() == "true":
				self.value_to_memory(quad[3], True)
			elif user_input.lower() == "false":
				self.value_to_memory(quad[3], False)
			else:
				print("Invalid value for input Bool")
				sys.exit(0)


		elif quad[1] == "Float":
			try:
				val = float(user_input)
				self.value_to_memory(quad[3], val)
			except ValueError:
				print("Invalid value for input Float")
				sys.exit(0)

		elif quad[1] == "Int":
			try:
				val = int(user_input)
				self.value_to_memory(quad[3], val)
			except ValueError:
				print("Invalid value for input Int")
				sys.exit(0)




	def goto(self, quad):
		self.iterators[-1] = quad[3] - 1

	def gotof(self, quad):
		if not self.value_from_memory(quad[1]):
			self.iterators[-1] = quad[3] - 1

	def era(self, quad):
		self.activation_record.append(dict())
		

	def param(self, quad):
		self.activation_record[-1][quad[3]] = self.value_from_memory(quad[1])

	def gosub(self, quad):
		self.function_memory.append(dict())
		for address in self.activation_record[-1].keys():
			self.value_to_memory(address, self.activation_record[-1][address])
		self.iterators.append(quad[1] - 1)
		self.activation_record.pop()

	def return_value(self, quad):
		self.value_to_memory(quad[3], self.value_from_memory(quad[1]))
		self.function_memory.pop()
		self.iterators.pop()

	def end_proc(self, quad):
		self.function_memory.pop()
		self.iterators.pop()

	def ver(self, quad):
		bottom_limit = quad[1]
		upper_limit = quad[2]
		value = self.value_from_memory(quad[3])
		if value < bottom_limit or value > upper_limit:
			print("Out of bounds")
			sys.exit(0)

			

	def end(self, quad):
		print("end")
		self.end_time = time.monotonic()
		print("Execution time: " + str((timedelta(seconds=self.end_time - self.start_time))))
		sys.exit(0)
