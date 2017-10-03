#This class manage 1 round of the game. One roung is composed of eigth tours. At the end of one round, each team wins
# a certain amount of points depending both on their contract and the points they have had. 

from global_values import *
from deck import Deck
from player import Player 

class Round_coinche():
	""" trump 			position in COLOR_LIST of trump choosen by contracted team										 constant for a round
		contract 		is the position (in CONTRACT_VALUES) of the number of points contracted-team claims it will had	 constant for a round
		contracted_team	0 for N_S and 1 for E_O								   							 				 constant for a round
		master 			is the master player who will strat the next tour(number in player_list)							variable
		pli				contains cards of current pli																		vairable """
		
	def __init__(self, trump, contract, contracted_team, dealer, players): 
		self.trump = trump
		self.contract = contract
		self.contracted_team = contracted_team
		self.master = (dealer+1)%4 #the player at left of dealer starts
		self.pli = []
		self.players = players

#	def play_round(self):
		
		
	def play_pli(self):
		self.pli = []
		for i in range (4) : 
			j = (i + self.master)%4
			print("ooooooooooooo"+"\n"+"o "+str(self.players[j])+" o"+"\n"+"ooooooooooooo")
			print("* "+"\n"+"Here is your hand, what do you want to play ?"+"\n"+str((self.players[j]).card))
			selected = input()
			self.pli.append(self.players[j].card[selected]) 
			del self.players[i].card[selected]
		
	



