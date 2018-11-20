 # -*-coding:Latin-1 -*
import socket 
import time
from global_values import *
import os
import sys
from Interface import *

# Le client ne fait pas réellement partie de la logique jeu, il recupère juste les informations pour les afficher au
# joueur et éventuellement retourner un choix que celui-ci fait. Le serveur n'écoute un client que lorsqu'il attend 
# quelque chose de lui (pas de multithread). A chaque fois que le serveur envoie une information au client celle-ci est précédée d'une 
# COMMANDE qui indique au client comment traiter l'information. Il attend ensuite une réponse spécifique ou non à la commande 
# envoyée (CHECK = simplement j'ai bien reçu). Lorsqu'on demande au client quelque chose on effectue les verifications de base
# du côté client c'est à dire que le type d'entrée est le bon et que sa valeur est possible (par exemple il n'y a pas de 
# couleur 4) mais les vérifications inérantes à la logique jeu sont réalisées du côté serveur, qui redemande une nouvelle
# valeur si celle qu'il a eu ne lui convient pas (par exemple si le joueur n'est pas monté à l'atout alors qu'il pouvait)


#       Head        --> tu es le joueur X                               ....... Fixé au début d'une partie est fixe tout le long
#       Head 2      --> Etat de la partie (TeamPoints)                  ....... Change entre chaque round (Display_game_informations)
#                       Phase à laquelle on en est (ENCHERE/ROUND)      ....... Change debut enchère et début round (Display_round_informations)
#           ___________________
#           |                  |
#           |                  |
#           |  Table de jeu    |                                        ........ Display_table_game
#           |                  |
#           |__________________|
#      [||||||||||||||||||||||||||||] --> cartes du joueur X            ........0 MyGameInListToString(MyGameInList)

# Head fixé pour tout une partie
# Head2 mis à jour à chaque phase du jeu 
# Affichage final 


head =""
head2 = "" 
PliOrBidAnnounces = ["","","",""]           #Systématiquement fourni a Display_table_game
PlayerNumber = -1000                              
speaker = -1000
mygameinlist = []
GraphPli = []
TeamPoints = [0,0]
try:
    print("Tentative de conection")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               # création de la socket 
    s.settimeout(4)                                                     # le client a 4s pour etre accepté par le serveur
    s.connect((HOST,int(PORT)))
    CanIPlay = None
    while CanIPlay!=WELCOME :                                           # en signe d'acceptation le serveur envoie WELCOME                                          
        CanIPlay = s.recv(TAILLE_BLOC)
    s.settimeout(None)
    while CanIPlay :
        data = s.recv(TAILLE_BLOC)
        if data :
            data = data.split(SEP)
            command = data[0]
            
            if command==INFO :                                          # Simple affichage d'information
                s.send((CHECK)) #aucune reponse
                os.system('cls' if os.name == 'nt' else 'clear')
                print(data[1])
                
            if command == GIVENUMBER :                                  # En début de partie on informe chaque joueur de sa place
                s.send((CHECK)) #aucune reponse
                PlayerNumber = int(data[1])
                head = "Tu es le joueur "+PLAYERS[PlayerNumber]             # on l'affichera ensuite systématiquement en haut de la fenêtre
                
            if command==STARTNEWPHASE :                                 # On commence un jeu, les enchères ou un round
                s.send((CHECK)) #aucune reponse
                if data[1] == GAME :                                    # Gère le cas de l'enchainement des games
                    PliOrBidAnnounces = ["","","",""]
                    mygameinlist = []
                if data[1] == BIDSTART :                                # Affichage dans le head2 qu'on est dans la phase enchère
                    head2 = head +"\n" + Display_game_informations(TeamPoints) +BIDDING
                    speaker = int(data[2])
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(head2 + "\n" + Display_table_game(PliOrBidAnnounces,speaker) + MyGameInListToString(mygameinlist))
                if data[1] == ROUNDSTART :                              # Affichage dans le head2 qu'on est dans la phase enchère
                    head2 = head + "\n" + Display_game_informations(TeamPoints) + Display_round_informations(data[2],data[3])
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(head2 + "\n" + Display_table_game(GraphPli,speaker) + MyGameInListToString(mygameinlist))
                        
            if command == UPDATEBID:                                    # Recoit enchère faite (par soit-même ou par les autres)
                s.send((CHECK)) #aucune reponse
                PliOrBidAnnounces[int(data[1])] += data[2]
                os.system('cls' if os.name == 'nt' else 'clear')
                print(head2 + "\n" + Display_table_game(PliOrBidAnnounces,0)+ MyGameInListToString(mygameinlist)) #en fait ya pas de speaker l'ordre n'est pas l'ordre joué
                
                
            if command == CURRENTBIDDING :                              # Informe le joueur qu'il doit joueur ou quel joueur joue
                s.send((CHECK)) #aucune reponse
                os.system('cls' if os.name == 'nt' else 'clear')
                if int(data[1]) == PlayerNumber : 
                    print(head2 + "\n" + "C'est a toi de jouer...\n"+Display_table_game(PliOrBidAnnounces,0)+ MyGameInListToString(mygameinlist))
                else : 
                    print(head2 + "\n" + "Le joueur "+PLAYERS[int(data[1])] + " est en train de jouer...\n"+ Display_table_game(PliOrBidAnnounces,0)+ MyGameInListToString(mygameinlist))
         
         
            if command == BIDORNOT :                                    # Demande au joueur s'il veux faire une enchère à son tour
                bid = 3
                while int(bid)!=1 and int(bid)!=0 :                        # Vérification que l'entrée possible (True/False)
                    while True :                                                            #gestion du bon type d'entrée (int)
                        bid = raw_input("Veux-tu faire une enchère ? oui(1), non(0)\n")
                        try : 
                            bid = int(bid)
                            break
                        except : 
                            print("Oops!  Ca s'était même pas un chiffre, essaye encore ....")
                s.send(ANSWERINGWANNAPLAY + SEP + str(bid)) # réponse de type ANSWERINGWANNAPLAY
                
                
                
            if command == PROPOSECONTRACT :                             # Demande de l'enchère qu'un joueur souhaite faire
                print(SHOW_BIDDINGS)
                value = 9000
                while value not in range (0,10):                           # range des valeurs d'enchère possibles (cf len CONTRACT)
                    while True :                                              # vérification du type d'entrée (int)
                        value = raw_input("Quelle est la valeur de ton contrat :")
                        try :
                            value = int(value)
                            break
                        except : 
                            print("Oops!  Tu n'as pas entré une enchère valide, essaye encore ....")
                            
                color = 9000
                while color not in range (0,4):                             # range des couleurs possibles  (cf COLOR_LIST)
                    while True :                                                # verification du type d'entré (int)     
                        color = raw_input("Quel atout choisis-tu :")
                        try :
                            color = int(color)
                            break
                        except : 
                            print("Oops!  Tu n'as pas entré une enchère valide, essaye encore ....")
                s.send(ANSWERINGCONTRACT + SEP + str(value) + SEP + str(color))              
                
            if command == CURRENTPLAYING :                                  # Analogue de CURRENTBIDDING pour la partie jeu
                s.send((CHECK)) #aucune reponse
                os.system('cls' if os.name == 'nt' else 'clear')
                if int(data[1]) == PlayerNumber :                              
                    print(head2 + "\n" + "C'est a toi de jouer...\n"+Display_table_game(GraphPli,speaker)+ MyGameInListToString(mygameinlist))
                else : 
                    print(head2 + "\n" + "Le joueur "+PLAYERS[int(data[1])] + " est en train de jouer...\n"+ Display_table_game(GraphPli,speaker)+ MyGameInListToString(mygameinlist))      
 
            if command == PLAYCARD :                                        #demande au joueur la carte qu'il veut jouer
                card = 9000
                while card not in range (0,len(mygameinlist)):              # verification que la carte existe dans la main
                    while True :                                                    
                        card = raw_input("Choisi une carte : (indique sa position 0-->" + str(len(mygameinlist)-1)+") : ")
                        try :
                            card = int(card)
                            break
                        except : 
                            print("Oops!  Tu n'as pas entré une position de carte valide, essaye encore ....")
                s.send(CARDCHOOSEN + SEP + str(card))
                
            if command == CARDWASPLAYED :                                   # une carte a été joué : tout le monde l'ajoute au pli
                s.send((CHECK)) #aucune reponse
                GraphPli.append(data[1])
                if int(data[2]) == PlayerNumber :                           # si le joueur reconnait que c'est lui qui l'a joué il la retire de sa main
                    mygameinlist.remove(data[1])
                    
            if command == ACARDOFYOURHAND :                                 # Le joueur recoit une carte de sa main, il l'ajoute
                s.send(CHECK) #aucune reponse
                mygameinlist.append(data[1])
                    
            if command == ENDPLI :                                          # informe les joueurs du gagnant et réinitialise GraphPli 
                s.send(CHECK)
                os.system('cls' if os.name == 'nt' else 'clear')
                print(head2 + "\n" + "Le joueur "+PLAYERS[int(data[1])] + " a gagné le dernier pli, il commencera donc le prochain\n"+ Display_table_game(GraphPli,speaker)+ MyGameInListToString(mygameinlist))      
                speaker = int(data[1])
                GraphPli = []

            if command == TEAMPOINTS :                                      # Mise a jour des points des équipes
                s.send(CHECK) #aucune reponse
                TeamPoints[0] += int(data[1])
                TeamPoints[1] += int(data[2])
                
            if command == WANNAPLAYAGAIN :                                 # envoyé dirrectement par le serveur et pas par game
                answer = 3
                while int(answer)!=1 and int(answer)!=0 :
                    while True : 
                        answer = raw_input("\n" + "Veux-tu refaire une partie ? oui(1), non(0)\n")
                        try : 
                            answer = int(answer)
                            break
                        except : 
                            print(head + "\n" + "Oops!  Ca s'était même pas un chiffre, essaye encore ....")
                s.send(ANSWERINGWANNADOOTHERGAME+ SEP + str(answer))

                    
            if command == GIVEWINNER :                                      # donne le gagnant, l'affichage depend de si le gagant fait
                TeamPoints = [0,0]                                          # partie de l'équipe de joueur ou non
                s.send((CHECK)) #aucune reponse
                if int(data[1]) == 0 :
                    if PlayerNumber == 0 or PlayerNumber == 2 :
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(head + "\n" + "Felicitation tu as gagné la partie \n") 
                    else : 
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(head + "\n" + "Tu as perdu, mais courage tu feras mieux la prochaine fois !\n") 
          
                elif int(data[1]) == 1 :
                    if PlayerNumber == 1 or PlayerNumber == 3 :
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(head + "\n" + "Felicitation tu as gagné la partie \n") 
                    else : 
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(head + "\n" + "Tu as perdu, mais courage tu feras mieux la prochaine fois !\n") 
                        
                elif int(data[1]) ==2 :
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(head + "\n" + "Egalité parfaite tout le monde est gagnant !\n")
                
            if command == BYEBYE :                                          # si le joueur souhaite arreter de jouer (WANNAPLAYAGAIN)
                print ("Merci d'avoir joué, à la prochaine !")              # après avoir bien reçu l'info le serveur lui dit de se déconnecter
                break                                                       
                     
                
except socket.timeout:                                                      #seulement invocable au début, après timeout  = None
    print("Désolé, la partie est pleine, ouvre un autre serveur et crée ta propre partie !")

except socket.error:
    e = socket.error
    #print("erreur dans l'appel a une methode de la classe socket: %s" % e)
    sys.exit(1)

finally:
    # fermeture de la connexion
    s.close()
print ("fin du client TCP")
