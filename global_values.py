#!/usr/bin/env python
# -*- coding: utf8 -*-

TEAMS = ("N_S","E_O")
VALUE_LIST = ("7","8","9","10","Valet","Dame","Roi","As") 
COLOR_LIST = ("carreau", "pique", "trefle", "coeur")
POINTS = (0,0,0,10,2,3,4,11)
POINTS_ATOUTS = (0,0,14,10,20,3,4,11)
CONTRACT_VALUES = ("80", "90", "100", "110", "120", "130", "140", "150", "160", "capot")
PLAYERS = ("N","S","E","O")
from_number_to_place = {0 : "N", 1 : "E", 2 : "S", 3 : "O" }
from_number_to_team = {0 : 0, 1 : 1, 2 : 0, 3:  1 }
from_team_number_to_name = {0 : "N/S", 1 : "E/O"}



SHOW_BINDINGS = "choose your contract : [x,y]"+"\n"+"x :"+"\t"+"carreau"+"\t"+ "pique"+"\t"+ "trefle"+"\t"+"coeur"+"\n"+"   "+"\t"+"  0"+"\t"+"  1"+"\t"+"  2"+"\t"+"  3"+"\n"+ "---------------------------------------------------------------------------------"+"\n"+ "y :"+"\t"+"80"+"\t"+ "90"+"\t"+ "100"+"\t"+ "110"+"\t"+ "120"+"\t"+ "130"+"\t"+ "140"+"\t"+ "150"+"\t"+ "160"+"\t"+ "capot"+"\n"+"   "+"\t"+" 0"+"\t"+" 1"+"\t"+" 2"+"\t"+" 3"+"\t"+" 4"+"\t"+" 5"+"\t"+" 6"+"\t"+" 7"+"\t"+" 8"+"\t"+" 9"

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
