from global_values import *

class Card():
	def __init__(self,value,color):
		if value not in VALUE_LIST :
			raise ValueError("invalid value")
		if color not in COLOR_LIST :
			raise ValueError("invalid color")
		self.value = value
		self.color = color
		
		
	def __repr__(self):
		return "%s|%s"%(self.value,self.color)
		
	def __str__(self):
		return "%s de %s"%(self.value,self.color)
		
		
		
