from global_values import*
from player import Player


slot_available = ["N","S","E","O"]
player=[]
for i in range (4) : 
	player.append(Player(slot_available))
	slot_available.remove(player[i].place)


#for pos in PLAYERS:
	
print(player)
	
	
