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
