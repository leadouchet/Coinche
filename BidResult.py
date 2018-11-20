# -*- coding: utf-8 -*-
import Bid 

# Résultat d'une enchère

class bidResult():
	def __init__(self,Bidding,TeamIndex):
		self.bid = Bidding                     # Contrat établie (dernière enchère effectuée)
		self.team = TeamIndex                  # Equipe ayant remporté les enchères
