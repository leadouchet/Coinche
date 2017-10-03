import random 
from card import Card
from global_values import*

class Deck():
	def __init__(self):
		self.card_list=[Card(VALUE_LIST[i],COLOR_LIST[j]) for i in range(8) for j in range(4)]


	def shuffle(self):
		random.shuffle(self.card_list)
		
	def cut(self):
		print("Where do you want to cut ? Choose a position betwenn 1 and 31"+"\n"+"______________________________________________________________________")
		coupe = input()
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
		

	



