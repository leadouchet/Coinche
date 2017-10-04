# -*- coding: utf-8 -*-
#This class manage 1 round of the game. One roung is composed of eigth tours. At the end of one round, each team wins
# a certain amount of points depending both on their contract and the points they have had.

from card import Card
from deck import Deck
import os 

import random
""" trump 			position in COLOR_LIST of trump choosen by contracted team										 constant for a round
    contract 		is the position (in CONTRACT_VALUES) of the number of points contracted-team claims it will had	 constant for a round
    contracted_team	0 for N_S and 1 for E_O								   							 				 constant for a round
    master 			is the master player who will strat the next tour(number in player_list)							variable
    pli				contains cards of current pli																		vairable """


from global_values import *
from player import Player
from player import Players

class Round_coinche() :
    def __init__(self, trump, contract, contracted_team, dealer, players):
		#constant attribute :
        self.trump = trump
        self.contract = contract
        self.contracted_team = contracted_team
        self.players = players
        
        #other attribute : 
        self.master = (dealer+1)%4 #the player at left of dealer starts
        self.cards_team0 = []
        self.cards_team1 = []
        self.pli = []
        self.contracted_team_points = 0
        self.other_team_points = 0
            
    def play_round(self) :
        for i in range(8) :
            self.play_pli()
            self.master = self.seek_master()
            if from_number_to_team[self.master] == 0 :
                self.cards_team0 += self.pli
            else :
                self.cards_team1 += self.pli

        self.points_compt()
        if self.contracted_team == 0 :
            return ([self.contracted_team_points,self.other_team_points], self.cards_team0+ self.cards_team1)
        else :
            return ([self.other_team_points,self.contracted_team_points], self.cards_team0+ self.cards_team1)



    def play_pli(self) :
        self.pli = []
        for i in range (4) :
            j = (i + self.master)%4
            os.system('cls' if os.name == 'nt' else 'clear')
            raw_input("oooooooooooo"+"\n"+"o "+str(self.players[j])+" o"+"\t"+"Contracted team : "+from_team_number_to_name[self.contracted_team]+"\t"+"Contract :" + CONTRACT_VALUES[self.contract]+ " " +COLOR_LIST[self.trump]+"\n"+"oooooooooooo")
            print(table_game(self.pli,self.master))
            print(" "+"\n"+"Here is your hand, what do you want to play ?"+"\n"+str((self.players[j]).card))
            selected = input()
            self.pli.append(self.players[j].card[selected])
            del self.players[j].card[selected]


    def strenght(self, card):
        if card.color == self.trump :
            return(12 + POINTS_ATOUTS[card.value])
        else :
            return(POINTS[card.value])


    def seek_master(self):
        master_card_index = 0
        for i in range(1,4) :
            if self.pli[i].color in [self.pli[0].color,self.trump] :
                if self.strenght(self.pli[i])> self.strenght(self.pli[master_card_index]):
                    master_card_index = i
        return((self.master + master_card_index)%4)

    def cards_point(self, cards) :
        points = 0
        for card in cards :
            if card.color == self.trump :
                points += POINTS_ATOUTS[card.value]
            else :
                points += POINTS[card.value]
        return(points)

    def points_compt(self) :
        points_team0 = self.cards_point(self.cards_team0)
        points_team1 = self.cards_point(self.cards_team1)
        if self.contracted_team == 0 :
            if self.contract <= 8 :                                                                         #if contract isn't capot
                if points_team0 >= int(CONTRACT_VALUES[self.contract]) :                                    #if won
                    self.contracted_team_points = points_team0 + int(CONTRACT_VALUES[self.contract])           #contract points + done points
                    self.other_team_points = points_team1
                else :                                                                                      #else
                    self.other_team_points = 162 + int(CONTRACT_VALUES[self.contract])
            else :
                if points_team0 == 162 :
                    self.contracted_team_points = 252 + 162
                else :
                    self.other_team_points = 162 + 162
        else :
            if self.contract <= 8 : #if contract isn't capot
                if points_team1 >= int(CONTRACT_VALUES[self.contract]) :
                    self.contracted_team_points = points_team1 + int(CONTRACT_VALUES[self.contract])
                    self.other_team_points = points_team0
                else :
                    self.other_team_points = 162 + int(CONTRACT_VALUES[self.contract])
            else :
                if points_team1 == 162 :
                    self.contracted_team_points = 252 + 162
                else :
                    self.other_team_points = 162 + 162





def table_game(pli,starter):
	table = ["","","",""]
	for i in range(4):
		j = (starter+i)%4
		if i<len(pli):
			table[j] = pli[i]
	l1 = "\t\t\t\t"+"[N]"+"\t\t\t\t\n"
	l2 = "\t\t\t\t"+str(table[0])+"\t\t\t\t\n"
	l3 = "[O]\t\t\t\t\t\t\t[E]\n"
	l4 = str(table[3])+"\t\t\t\t\t\t\t"+str(table[1])+"\n"
	l5 = "\t\t\t\t"+"[S]"+"\t\t\t\t\n"
	l6 = "\t\t\t\t"+str(table[2])+"\t\t\t\t\n"
	return(l1+l2+l3+l4+l5+l6)
	

	



