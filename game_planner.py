
from player import Player
from player import Players
from make_binddings import make_binddings
from round_coinche import Round_coinche
from global_values import *
import random







def Game_planner():
	players = Players()
	#teams = [[0,2],[1,3]]
	teams_points = [0,0]
	dealer = random.randint(0,3)
	print(dealer)
	while teams_points[0]<2000 and teams_points[1]<2000 : 
		contracted_team,contract = make_binddings(dealer) #a team (0 or 1) and a value of contract (couleur,valeur)
		current_round = Round_coinche(contract[0],contract[1],contracted_team,dealer,players)
		for i in range(8):
			current_round.play_pli()
		dealer = (dealer + 1)%4
			
		
		
		
		
		
		
		dealer += 1 
	






Game_planner()



	
	
	
