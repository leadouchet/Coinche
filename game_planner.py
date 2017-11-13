# -*- coding: utf-8 -*-
#COUCOU FLORIANT je tente de comprendre git et visual studio


#class
from player import Player
from player import Players
from round_coinche import Round_coinche
from deck import Deck

#constant
from global_values import *

#packages
import random
import os 



def binding_to_string(binding):
    if binding == None:
        return("Pass")
    else : 
        return(CONTRACT_VALUES[binding[1]]+" "+COLOR_LIST[binding[0]])
        

def Game_planner():
    players = Players()
    players.order_players()
    teams_points = [0,0] #[N_S : 0, E_O :1]
    dealer = random.randint(0,3)
    cards = Deck()
    cards.shuffle()
    while teams_points[0]<2000 and teams_points[1]<2000 :
        
        #Cards distribution
        lots = cards.distribute_deck()
        for i in range (4) :
            players[(dealer + 1 + i)%4].card = lots[i]
        players.order_cards()
        
        #Binddings
        bindings = []
        finisher = -1 #on first tour, 4 people have to pass so that binddings end
        print("ooooooooooooooooooo"+"\n"+"o    BINDINGS     o" + "\n""ooooooooooooooooooo")

        speaker = (dealer+1)%4
        #DEBBUG = False
        contract = None
        contracted_team = None
        while finisher<3:
        #while not DEBBUG :
            
            os.system('cls' if os.name == 'nt' else 'clear')
            raw_input("\n"+"Player "+from_number_to_place[speaker]+" it's your turn, type enter to see your cards :" )
            print(finisher)
            print(table_game(bindings,(dealer+1)%4))
            print(players[speaker].card)
            print("\n"+"Player "+from_number_to_place[speaker]+" do you want to make a binding ? Yes (1) No (2)")
            wanna_play = input()
            if wanna_play == 1 :
                print(SHOW_BINDINGS)
                contract = input()
                contracted_team = from_number_to_team[speaker] #can take value 0 or 1 
                finisher = 0
                #DEBBUG = True

            else :
                finisher += 1
            bindings.append(binding_to_string(contract))
                    
            speaker = (speaker + 1)%4
        
        if contract!=None :      
        #Round
            print("oooooooooooooo"+"\n"+"o    GAME     o" + "\n""oooooooooooooo")
            current_round = Round_coinche(contract[0],contract[1],contracted_team,dealer,players)
            round_points, list_cards = current_round.play_round()
            cards.upload_deck(list_cards)
            print("Where do you want to cut ? Choose a position betwenn 1 and 31"+"\n"+"______________________________________________________________________")
            coupe = input()
            cards.cut(coupe)
            teams_points[0] += round_points[0]
            teams_points[1] += round_points[1]
		#update
            dealer = (dealer + 1)%4
            print(teams_points)
		
        else : 
            print("Nobody made a binding, let's distribute again")


"""players = Players()
teams_points = [0,0]
dealer = random.randint(0,3)
cards = Deck()
cards.shuffle()
lots = cards.distribute_deck()
for i in range (4) :
    players[(dealer + 1 + i)%4].card = lots[i]

speaker = (dealer+1)%4

raw_input("\n"+"Player "+from_number_to_place[speaker]+" it's your turn, type enter to se your cards :" )
print(players[speaker].card)
print("\n"+"Player "+from_number_to_place[speaker]+" do you want to make a binding ? Yes (1) No (2)")
"""
Game_planner()



        
