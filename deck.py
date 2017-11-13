# -*- coding: utf-8 -*-
import random
from card import Card
from global_values import*

class Deck():
	def __init__(self):
		self.card_list=[Card(i,j) for i in range(8) for j in range(4)]
  	def upload_deck(self,list_cards):
        	self.card_list = list_cards
	def shuffle(self):
		random.shuffle(self.card_list)
		
	def cut(self, coupe):
		if (coupe<1) or (coupe>31) :
			coupe = random.randint(1,31)
		print("You choosed an invalid place, I choosed randomly for you the place "+str(coupe))
		self.card_list = self.card_list[coupe:]+self.card_list[:coupe]
		
	def distribute_deck(self):
		scheme = [3,2,3]
		lots = [[] for i in range(4)]
		for card_number in scheme :
			for lot_number in range(4) : 
				lots[lot_number].extend(self.card_list[0:card_number])
				self.card_list=self.card_list[card_number:]
		return lots
		

