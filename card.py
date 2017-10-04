from global_values import *

class Card():
	def __init__(self,value,color):
		self.value = value
		self.color = color
		
		
	def __repr__(self):
		return "%s:%s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])
		
	def __str__(self):
		return "%s de %s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])
		
		
		
