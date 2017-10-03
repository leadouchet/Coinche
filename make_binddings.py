
from global_values import *
def make_binddings(dealer):
	finisher = -1 #on first tour, 4 people have to pass so that binddings end
	print("ooooooooooooooooooo"+"\n"+"o    BINDINGS     o" + "\n""ooooooooooooooooooo")
	contract = None
	contracted_team = None
	speaker = (dealer+1)%4
	while finisher<3:
		print("\n"+"Player "+from_number_to_place[speaker]+" do you want to make a binding ? Yes (1) No (2)")
		wanna_play = input()
		if wanna_play == 1 :
			print("choose your contract : [x,y]")
			print("x :"+"\t"+"carreau"+"\t"+ "pique"+"\t"+ "trefle"+"\t"+"coeur"+"\n"+"   "+"\t"+"  0"+"\t"+"  1"+"\t"+"  2"+"\t"+"  3")
			print("---------------------------------------------------------------------------------")
			print("y :"+"\t"+"80"+"\t"+ "90"+"\t"+ "100"+"\t"+ "110"+"\t"+ "120"+"\t"+ "130"+"\t"+ "140"+"\t"+ "150"+"\t"+ "160"+"\t"+ "capot"+"\n"+"   "+"\t"+" 0"+"\t"+" 1"+"\t"+" 2"+"\t"+" 3"+"\t"+" 4"+"\t"+" 5"+"\t"+" 6"+"\t"+" 7"+"\t"+" 8"+"\t"+" 9")
			contract = input()
			contracted_team = from_number_to_team[speaker]
			finisher = 0 
		else : 
			finisher += 1
				
		speaker = (speaker + 1)%4
	print("ooooooooooooooo"+"\n"+"o    GAME     o" + "\n""ooooooooooooooo")
	return(contracted_team,contract)

		
