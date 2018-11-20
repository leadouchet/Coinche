#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import socket
import os
from global_values import*
from Game import Game 
import signal

# Le serveur attend d'avoir 4 connexions pour lancer une parties. Les sockets sont dirrectement passées à la classe GAME.
# Afin de gérer le cas ou un 5ème client tenterait de se connecter, le serveur previent le client lorsqu'il accepte sa connection.
# Le while True permet de joue rdes parties en boucle (si les joueurs le souhaite), et d'accepter de nouveau client 
# si certains souhaitent continuer et d'autre arreter à la fin d'une partie

listeClient=[]


if __name__=="__main__":
    try : 
        print ("usage : %s <port>" % (PORT))
        # creation de l objet socket qui gerera les demandes d acces client (methode client "connect")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('',int(PORT)))
        sock.listen(0)

        while True :                                # permet de donner la possibilité aux joueurs de rejoué meme si cetains quittent
            while len(listeClient)<NBR_PLAYER:
                clisock, addr = sock.accept()
                clisock.send(WELCOME)               # indication comme quoi le serveur a bien recu la connection (gestion des connections alors que la partie est pleine)
                listeClient.append(clisock)
                print ("connection entrante : "+ str(addr))
                for c in listeClient :
                    c.send(INFO + SEP + "Le jeu commencera des que vous serez  "+ str(NBR_PLAYER) +" joueurs, pour le moment vous etes " + str(len(listeClient)))
                    check=c.recv(TAILLE_BLOC)
            for c in listeClient :
                c.send(INFO+SEP+"Le jeu va commencer....")
                check = c.recv(TAILLE_BLOC)
            time.sleep(4)                           # Pause de 4s avant de lancer le jeu
            WannaPlay = True
            while WannaPlay :                       # Wannaplay peut changer de valeur a chaque fin de partie
                game = Game(listeClient)
                game.Play()
                time.sleep(2)
                DoYouWantToPLayAgain = [False,False,False,False]
                ClientToDel = []
                for i in range (NBR_PLAYER):
                    listeClient[i].send(WANNAPLAYAGAIN)             # On demande en même temps à tous les clients (pour ne pas laisser l'affichage de fin de partie)
                for i in range (NBR_PLAYER):                        # et ensuite on récupère client par client
                    command = None
                    while command != ANSWERINGWANNADOOTHERGAME:     # on cherche a recevoir une commande de type ANSWERINGWANNADOOTHERGAME
                        data = listeClient[i].recv(TAILLE_BLOC)
                        data = data.split(SEP)
                        command = data[0]
                    DoYouWantToPLayAgain[i] =  bool(int(data[1]))
                    if DoYouWantToPLayAgain[i] == False :           # si une joueur ne veut pas rejouer, on l'ajoute a la liste des clients a supprimer et on lui dit de fermer sa socket et on la femre cote serveur
                        ClientToDel.append(i)
                        WannaPlay = False
                        listeClient[i].send(BYEBYE)
                        listeClient[i].close()
            newListClient = []                                      # liste des clients qui veulent continuer de jouer
            for i in range (NBR_PLAYER):
                if i not in ClientToDel:
                    newListClient.append(listeClient[i])
            listeClient = newListClient
            if len(listeClient) == 0 :                              # si aucun client ne souhaite continuer on ferme le serveur
                print("Tous les joueurs ont quité le jeu, on ferme le serveur")
                break
            
            for c in listeClient :                                  # on retourne dans le tant qu'il n'y a pas assez de joueur et on en informe les joueurs restants
                c.send(INFO + SEP + "Le jeu recommencera des que vous serez "+ str(NBR_PLAYER) +" joueurs, pour le moment vous etes " + str(len(listeClient)))

    finally : 
        sock.close()
    



