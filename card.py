# -*- coding: utf-8 -*-
from global_values import *

# Carte

class Card():
	def __init__(self,value,color):
		self.value = value                 # Valeur de la carte
		self.color = color                 # Couleur de la carte


	# Méthode permettant de représenter in carte via la méthode print
	def __repr__(self):
		return "%s:%s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])


	# Méthode qui convertit une carte en chaine de caractère
	def __str__(self):
		if (self.color == 0) or (self.color == 2):
			return "\033[1;7m" + "%s de %s"%(VALUE_LIST[self.value],COLOR_LIST[self.color]) + "\033[0m"
		else:
			return "\033[1;7;41m" + "%s de %s"%(VALUE_LIST[self.value],COLOR_LIST[self.color])+ "\033[0m"
