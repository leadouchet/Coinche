#!/usr/bin/env python
# -*- coding: utf8 -*-

#Toutes les constantes sont stockées ici afin qu'elles puissent être facilement modifiée.
# Par convention toutes les constantes sont en MAJUSCULESS.

###########################   Constantes d'affichage   ###########################
TEAMS = ("N_S","E_O")
VALUE_LIST = ("7","8","9","10","Valet","Dame","Roi","As") 
COLOR_LIST = ( "trefle", "carreau", "pique", "coeur")
CONTRACT = ("80", "90", "100", "110", "120", "130", "140", "150", "160", "capot")
PLAYERS = ("N","E","S","O")

###########################    Constantes de la logique jeu    ####################

NBR_PLAYER = 4  #4 en théorie mais moins possible pour mode debeug 
POINTS = (0,0,0,10,2,3,4,11)
STRENGH = (1,2,3,7,4,5,6,8)
POINTS_ATOUTS = (0,0,14,10,20,3,4,11)
STRENGH_ATOUTS = (100,200,700,500,800,300,400,600)
CONTRACT_VALUES = (80, 90, 100, 110, 120, 130, 140, 150, 160, 252)
FROM_NUMBER_TO_TEAM = {0 : 0, 1 : 1, 2 : 0, 3:  1 }
POINTSGAME =  2000

###########################   Constantes pour le réseau   #########################

#Paramètres de connection
TAILLE_BLOC = 1024
HOST = ""
PORT = 8000

###Protocole de communication

#séparateur pour le .split a réception du message
SEP = "/"


#Commandes envoyées depuis le serveur reconnu par le client 
WELCOME = "bienvenido"
INFO = "justdisplayit"
GIVENUMBER = "hereismyplace" 
STARTNEWPHASE = "newphaseaboutostart" #truc qui est affiche tout le temps, en haut de toutes les fenetres 
ROUNDSTART = "letsgobitches"
BIDSTART = "biddinggannastart"
BIDORNOT = "tobidornottobid"
UPDATEBID = "update bid"
CURRENTBIDDING = "biddingpers"
PROPOSECONTRACT = "contract"
UPDATEPLI = "Playerplayedacard"
CURRENTPLAYING = "informwhoplay"
PLAYCARD = "whatcardwannaplay"
ENDPLI = "capricestfini"
CARDWASPLAYED = "acardwasplayed"
ACARDOFYOURHAND = "addthishand"
GAME = "cleanmoiall"
ENDPLI = "endofpli"
TEAMPOINTS = "voilaVospoints"
WANNAPLAYAGAIN = "Onrecommence"
BYEBYE = "alaprochaine"
GIVEWINNER = "hereiswhowon"



#Commandes envoyées depuis le client reconnues par le serveur
CARDCHOOSEN = "Iwannaplaythiscard"
ANSWERINGWANNAPLAY = "doIwantToPlay"
ANSWERINGCONTRACT ="WHatContractDoIWantToDo"
ANSWERINGWANNADOOTHERGAME = "oupas"
CHECK = "200"

