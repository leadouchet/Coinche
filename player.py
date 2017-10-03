#a player owns cards and have a position on the table 

from global_values import *
import random


#class of 1 players
class Player():
	def __init__(self,slot_available):
		self.card = []
		self.place = automatic_slot(slot_available) 			#choose_slot(slot_available)
		while self.place not in PLAYERS or self.place not in slot_available :
			print("\n"+"*****************"+"\n"+"* INVALID PLACE *"+"\n"+"*****************"+"\n")
			self.place = choose_slot(slot_available)

	def __repr__(self):
		return "Player %s"%(self.place)
	def __str__(self):
		return "Player %s"%(self.place)


#class of 4 players, allows creating easly 4 players 

class Players():
	def __init__(self):
		self.players = []
		self.slot_available = list(PLAYERS)
		for i in range(4):
			self.players.append(Player(self.slot_available))
			self.slot_available.remove(self.players[i].place)		
	def aff(self):
		for i in range (4):
			print(self.players[i])
		
	def order_players(self):
		ordered_players=[None,None,None,None]
		for i in range (4) : 
			new = self.players[i]
			if new.place == "N":
				ordered_players[0]=new
			elif new.place =="E":
				ordered_players[1]=new
			elif new.place =="S":
				ordered_players[2]=new	
			else :
				ordered_players[3]=new
		self.players = ordered_players			



def choose_slot(slot_available):
	print("The following place are still available : ")
	print(slot_available)
	print("Choose where you wanna play : (S will play with N and E will play with O by default)" +"\n"+"______________________________________________________________________")
	place = input()
	return(place)
	
	
def automatic_slot(slot_available):
	return(random.choice(slot_available))
	
	

