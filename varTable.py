# ------------------------------------------------------------
# varTable.py
#
# Luis Salomon Flores Ugalde | A00817435
# Diego Contreras            | A00817441
# ------------------------------------------------------------
from copy import deepcopy
from objects import ObjectTable


class Var:
	def __init__(self, type, scope, private, value, address):
		self.type    = type
		self.scope   = scope
		self.private = private
		self.value   = value
		self.address = address

	def deepcopy(self):
		return deepcopy(self)


class VarTable:
	def __init__(self):
		self.directory = dict()
		self.objects = ObjectTable()

	# it will be program.Objects[key] = object
	def __set__(self, key, var):
		self.directory[key] = var

	def __getitem__(self, key):  # it will be program.funDir[funKey][varKey] and not program.funDir.get(key).varTable[key]
		return self.directory[key]

	# overload ->  key in program.varDir
	def __contains__(self, key):
		return key in self.directory

	def deepcopy(self):
		return deepcopy(self)
