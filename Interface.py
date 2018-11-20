
# -*- coding: utf8 -*-
from global_values import*

                #################################################################
                # Ensemble des fonctions premettant l'affichage dans le terminal#
                #################################################################

# ECRANT TERMINAL TYPE :

#       Head 2      --> Etat de la partie (TeamPoints)                  ....... Change entre chaque round (Display_game_informations)
#                       Phase à laquelle on en est (ENCHERE/ROUND)      ....... Change debut enchère et début round (Display_round_informations)
#           ___________________
#           |                  |
#           |                  |
#           |  Table de jeu    |                                        ........ Display_table_game
#           |                  |
#           |__________________|
#      [||||||||||||||||||||||||||||] --> cartes du joueur X            ......... MyGameInListToString(MyGameInList)



# Permet d'afficher la table de jeu avec les cartes jouées lors d'un plis ou les enchères effectuées 
# plutot ecrite pour représenter un pli : première carte posée par le starter nécessité de le connaitre
# pour associer la bonne carte à la bonne personne. Peut également être utilisée pour afficher enchères
# en donnant comme starter 0 (en effet les enchères sont initialisées comme une 4liste vide).
def Display_table_game(pli,starter):
    table = ["","","",""]
    for i in range(NBR_PLAYER):
        j = (starter+i)%NBR_PLAYER
        if i<len(pli):
            table[j] = pli[i]
    l1 = "\t\t\t\t\t"+"[N]"+"\t\t\t\t\n"
    l2 = "\n\t\t\t\t\t"+str(table[0])+"\t\t\t\t\n"
    l3 = "\t[O]\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t[E]\n"
    l4 = "\t"+str(table[3])+"\n\t\t\t\t\t\t\t\t"+str(table[1])+"\n"
    l5 = "\t\t\t\t\t"+"[S]"+"\t\t\t\t\n"
    l6 = "\n\t\t\t\t\t"+str(table[2])+"\t\t\t\t\n"
    return(l1+l2+l3+l4+l5+l6+"\n")


# Affichage des informations du round 
def Display_round_informations(team,contract):
    l1 = "\t\t\t\tooooooooooooooooooooooooooooooooo\n"
    l2 = "\t\t\t\to\t\tROUND\t\to\n"
    l3 = "\t\t\t\to-------------------------------o\n"
    l4 = "\t\t\t\to Team : \t"+team+"\t\to\n"
    l5 = "\t\t\t\to Contract : \t"+contract+"\to\n"
    l6 = "\t\t\t\tooooooooooooooooooooooooooooooooo\n"
    return('\033[1m' + l1+l2+l3+l4+l5+l6 + '\033[0m')


# Affichage des informations de la partie
def Display_game_informations(TeamPoints):
    #l1 = "\t\t\tooooooooooooooooooooooooo\n"
    l2 = "\t\t\t\t\tGAME\t\n"
    l3 = "\t\t\t\t-------------------\n"
    l4 = "\t\t\t\t Team N/S: \t"+str(TeamPoints[0])+"\t\n"
    l5 = "\t\t\t\t Team E/O:\t"+str(TeamPoints[1])+"\t\n"
    #l6 = "\t\t\tooooooooooooooooooooooooo\n"
    return('\033[1m' +l2+l3+l4+l5 + "\n" + '\033[0m')



# Tag dans le head2 pour signifier qu'on est pendant la phase enchère
BIDDING = '\033[1m' + "\t\t\t\tooooooooooooooooooo"+"\n"+"\t\t\t\to    Enchères     o" + "\n""\t\t\t\tooooooooooooooooooo\n" + '\033[0m'

# Affichage des enchères eventuellement possible (ne prends pas en compte ce qui a été fait avant) 
SHOW_BIDDINGS = '\033[1m' +"Choisis ton contract : \n"+"\n"+"Atout :"+"\t"+"trefle"+"\t"+ "carreau"+"\t"+ "pique"+"\t"+"coeur"+"\n"+"   "+"\t"+"  0"+"\t"+"  1"+"\t"+"  2"+"\t"+"  3"+"\n"+ "---------------------------------------------------------------------------------"+"\n"+ "valeur :"+"\t"+"80"+"\t"+ "90"+"\t"+ "100"+"\t"+ "110"+"\t"+ "120"+"\t"+ "130"+"\t"+ "140"+"\t"+ "150"+"\t"+ "160"+"\t"+ "capot"+"\n"+"   "+"\t\t"+" 0"+"\t"+" 1"+"\t"+" 2"+"\t"+" 3"+"\t"+" 4"+"\t"+" 5"+"\t"+" 6"+"\t"+" 7"+"\t"+" 8"+"\t"+" 9" + '\033[0m'

# Transforme une enchère de type bid (ou None si pas d'enchère) en string
def bidding_to_string(binding):
    if binding == None:
        return("Pass")
    else : 
        return(CONTRACT[binding.value]+" "+COLOR_LIST[binding.color])

# Transforme une liste de string en un seul string. On ne peut pas utiliser la fonction pas défault car elle ne
# permet pas d'afficher les couleurs
def MyGameInListToString(MyGameInList):
    string = "["
    for i in range (len(MyGameInList)):
        string += "  " + MyGameInList[i] 
    return(string + "  ]")
