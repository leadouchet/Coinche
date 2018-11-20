# -*- coding: utf-8 -*-
from BidResult import bidResult 
from deck import Deck
import random as rd
from global_values import*
from PliResult import PliResult 
from Bid import Bid 
from Interface import*
import os
import time

# La classe Game est la plus importante du projet. Elle gère toute la logique jeu et est dirrectement lié à la logique réseau puisqu'elle possède comme attribu 
# la liste des sockets clients. Voir client et serveur pour plus d'informations sur la partie réseau. 

class Game():
    def __init__(self,ListeClient):
        self.teamGamePoints = [0,0]                 # List(int) [pointTeam NS, pointTeam EO]
        self.deck = Deck()                          # objet de type Deck, le jeu de carte
        self.deck.shuffle()                         # On mélange le Deck crée, unique appel de cette méthode car on ne mélange pas entre deux round 
        self.twoStacks = [[],[]]                    # 2 listes de cartes, correspondant aux cartes jouées par chaque équipe au cours d'un round
        self.hands = [[],[],[],[]]                  # liste contenant 4 listes de cartes  = les mains des 4 joueurs, dans l'ordre : N, E, S, O
        self.listeClient = ListeClient              # Liste des sockets clients des 4 joueurs 
        #self.dealer = rd.randint(0,NBR_PLAYER-1)   # choix aléatoire du premier dealer (jouer qui distribue)
        self.dealer = 0                             # choix fixe du premier dealer : joueur nord
        
        
                            #############################################################################
                            ############################ Logique du jeu #################################
                            #############################################################################
                            
                            

# Joueur un jeu = jouer x rounds jusqu'à ce qu'une des deux equipes aie 2000 pts (ou autre, nombre de points à fixer dans global value)
# détermine l'équipe gagnant 

    def Play(self):                                     
        self.SendTheirPosToPlayer()
        while (self.teamGamePoints[0]<POINTSGAME and self.teamGamePoints[1]<POINTSGAME):       
            roundResults = self.PlayRound()                                                   #   joueur un round 
            for i in range (2) :                                                              #   ajouter les points gagnés au score des teams respectives
                self.teamGamePoints[i] += roundResults[i]            
            self.SendTheirTeamPointsToPLayer()
            self.deck.stackToDeck(self.twoStacks)                                            #   On reforme le deck à partir des deux tas formés par chaque team 
            if len(self.deck.card_list) != 32 :                                                        #   S'il n'y a pas 4 joueurs on est obligé de recreer un deck 
                self.deck = Deck()                                                           #   (l'association des tas du round precedent ne donne pas assez de carte)
                self.deck.shuffle()                                                               
            self.dealer = self.Next(self.dealer)
            
        Winner = self.WhoWonTheGame()                                                         #   return 0 (la team NS a gagné), 1(la team EO a gagné) ou 2 (les deux teams ont gagné)
        for i in range (NBR_PLAYER):
            self.listeClient[i].send(GIVEWINNER + SEP + str(Winner))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i) 
        return()


# Le jeu se resume donc a jouer un ensemble de round. Un round est constitue d'enchere puis de 8 tour de jeu 
# Cette fontion retourne un round result c'est a dire une 2-liste [point team NS , point team EO]
# On commence pas distribuer le jeu avant de faire des enchères
# Les resultats des encheres sont stockés dans un objet de type BidResult qui contient l'enchère finale et la team qu'il 
#l'a faite. Dans le cas ou personne n'a pris (aucun joueur n'a fait d'enchère --> bidRes = None) on recommence, c'est a dire
# on change le dealer, on reforme le deck a partir des 4 mains des joeurs (sans mélanger !!!), et on recommence.
# Si le joueur a pris, on informe les clients que le round commence + envoie information a afficher (team qui a pris, quel contratct)


    

    def PlayRound(self):
        self.InformClientsNewGameStart()
        self.hands = self.deck.distribute_deck()
        self.sendTheirHandToPlayers()                    
            
        roundResults = [0,0]                            # points marqués à la fin d'un round par les teams 1 et 2 à la fin du round
        teamPoints = [0,0]                              # points marqués au fur et à mesure du round
        bidRes = self.PlayBidding()
        if (bidRes == None):                            # si aucune enchère n'a été faite
            self.deck.stackToDeck(self.hands)
            self.dealer = self.Next(self.dealer)
            return(self.PlayRound())
        else : 
            self.InformClientsFinalBid(bidRes)
            starter = self.Next(self.dealer)
            for i in range (8):                         # un round = 8 plis
                result = self.PlayPli(bidRes,starter)
                self.informClientsPliWinner(str(result.player))
                time.sleep(4)   
                teamPoints[FROM_NUMBER_TO_TEAM[result.player]] += result.points
                starter = result.player
                if (i==7):                                                          #Si c'est le dernier pli d'un round il y a le 10 de der : +10 points pour le gagnant
                    teamPoints[FROM_NUMBER_TO_TEAM[result.player]] += 10
            if (teamPoints[bidRes.team]>= CONTRACT_VALUES[bidRes.bid.value] ) :                                 #A la fin d'un round on attribue les les points a chaque team en fonction du contract annoncé
                roundResults[bidRes.team] = teamPoints[bidRes.team] + CONTRACT_VALUES[bidRes.bid.value]
                roundResults[(bidRes.team+1)%2] = 162 - teamPoints[bidRes.team]
            else :
                roundResults[bidRes.team] = 0
                roundResults[(bidRes.team+1)%2] = 162 + CONTRACT_VALUES[bidRes.bid.value]
            return(roundResults)



# Lors d'un pli chaque joueur jouer une carte en commençant par le gagnant du pli précédent (ou le jouer a gauche du dealer pour le premier plis)
# Cette méthode retourne un objet de type pliResult


    def PlayPli(self,bidRes,first):
        pli = []
        speaker = first
        for i in range (NBR_PLAYER):
            currentPlayer = (speaker + i)%NBR_PLAYER
            self.InformClientCurrentPlayer(currentPlayer)
            IsCardPlaceValid = False
            CardPlaceValid = self.CardsICanPlay(bidRes.bid.color,pli,self.hands[currentPlayer])             # methode de verification des regles du jeu : gènere une liste de la position des cartes qu'il peut jouer
            
            while not IsCardPlaceValid :                                                                    # le temps que la carte n'est pas valide on redemande une carte
                self.listeClient[currentPlayer].send(PLAYCARD)
                CardPlace = self.receivedFromPlayer(CARDCHOOSEN,currentPlayer)[1]
                IsCardPlaceValid = int(CardPlace) in CardPlaceValid

            self.InformPlayerACardWasPlaced(currentPlayer,CardPlace)                                        # informe la carte joué et par qui 
            pli.append(self.hands[currentPlayer][int(CardPlace)])
            del self.hands[currentPlayer][int(CardPlace)]                                                   # retire la carte joué de la main du joueur 
            
        pliRes = self.GetPliResult(bidRes.bid.color, pli, speaker)                                          # Retourne un PliResult (player et point)
        for card in pli :                                                                                   # Mets le pli dans le tas de la team qui l'a gagné
            self.twoStacks[FROM_NUMBER_TO_TEAM[pliRes.player]].append(card)
        return(pliRes)
        
            
# Lors des enchères les joueurs parlent chacun leur tour pour faire une enchère dont la valeur doit être supérieur à celles déjà faites
# retourne none si aucune enchère n'a été fait
# retourne BidResult si une enchere a était daite
    
    def PlayBidding(self):                                                                        
        speaker  = self.Next(self.dealer)
        self.InformClientsBidStart(speaker)
        biddings = []                                                                            # liste de toutes les enchères
        finisher = -1                                                                            # compte le nombre de passe à la suite, démare à -1 pour gérer cas particulier du 4 passes à la suite
        bestBid = None                                                                           # permet de savoir rapidement si une enchère a été faite et quelle est le joueur qui l'a faite
        while (finisher !=NBR_PLAYER-1):                                                         # tant qu'il n'y a pas eu 3 passes ou 4 passes au premier tour
            self.InformClientsCurrentBidder(speaker)
            self.listeClient[speaker].send(BIDORNOT)
            wannaPlay = self.receivedFromPlayer(ANSWERINGWANNAPLAY,speaker)[1]                   # on demande au joueur s'il veut jouer
            if int(wannaPlay) :
                bid = Bid()                                                                      # il va faire une enchère on crée donc une instance d'enchère
                IsBidValid = False                  
                while not IsBidValid :                                                           # check s'il a bien le droit de faire l'enchère (obligation de monter)
                    self.listeClient[speaker].send(PROPOSECONTRACT)
                    received = self.receivedFromPlayer(ANSWERINGCONTRACT,speaker)[1:]
                    bid.value = int(received[0])
                    bid.color = int(received[1])
                    IsBidValid = self.testBid(biddings,bid)
                bestBid = speaker                                                               # au moment ou le joueur fait une enchère s'est forcément la meilleure
                if bid.value == 9:                                                              # si quelqu'un annonce capot les enchères sont finies (on ne peut pas d'enchere plus haute) on lance le jeu 
                    return(bidResult(bid,FROM_NUMBER_TO_TEAM[bestBid]))                         
                biddings.append(bid)
                finisher = 0                                                                    # quelqu'un a fait une enchère on remet le compteur des passes à 0
                self.UpdatePlayersGraphBid(speaker,bidding_to_string(bid)+" | ")                
            else : 
                finisher += 1
                self.UpdatePlayersGraphBid(speaker,"pass | ")
            speaker = self.Next(speaker)

        if (bestBid != None) :                                                      # s'il y a eu au moins une enchère de faite
            return(bidResult(biddings[-1],FROM_NUMBER_TO_TEAM[bestBid]))            # on retourne la derniere enchère et le dernier joueur à avoir faite une enchère
        else :                                                                      
            return None                                                             # aucune enchère n'a été faite 



                            #############################################################################
                            ############################ Méthodes annexes ###############################
                            #############################################################################


#Test si une enchère que souhaite faire un joueur est valable (pas si elle existe puisque c'est verifié dans le client, seulement si elle est supérieure à celles faites avant)
    def testBid(self,biddings,bid):
        if len(biddings) == 0 :                                     #Si aucune enchère n'a été faites, l'enchère que souhaite faire le joueur est forcément valable
            return(True)
        else :
            if biddings[len(biddings)-1].value < bid.value :        # sinon on vérifie qu'elle est de valeur supérieur à celle de la dernière enchère
                return(True)
        return(False)


# Permet a part d'un plis de l'atout et du joueur qui a commencé de retourner un PliResult (player/points)
# On distingue les points que donne une carte de la force qu'elle a puisque par exemple, un atout à toujours une force supérieur à une carte non atout
# Voir les constantes STRENGH_ATOUT et STRENGH dans global_value.py pour plus d'information à ce sujet
    def GetPliResult(self,atout, pli, starter):
        cardStrength = [0,0,0,0]
        cardPoints = [0,0,0,0]
        for i in range (NBR_PLAYER):
            if(pli[i].color == atout):                               # si le couleur d'une carte est celle de l'atout sa force et ses points sont constants
                cardStrength[i] = STRENGH_ATOUTS[pli[i].value] 
                cardPoints[i] = POINTS_ATOUTS[pli[i].value]
            else:
                cardPoints[i] = POINTS[pli[i].value]                 # sinon ses points sont constants MAIS
                if (pli[i].color == pli[0].color):                   # sa force dépend de si sa couleur était bien la couleur demandée
                    cardStrength[i] = STRENGH[pli[i].value]
                else :  
                    cardStrength[i] = 0                              # car sinon sa force est nule 
        return(PliResult((starter+cardStrength.index(max(cardStrength)))%NBR_PLAYER,sum(cardPoints)))
    
# Methodes permettant de dire à un moment d'un plis quel cartes un joueur peux jouer, retourne liste des positions dans sa mains des cartes qu'il peut jouer
# N'a pas été fait ici mais permettrait relativement facilement d'implémenter une IA naive mais respectant les règles du jeu
# se référer aux règles du jeu pour bien comprendre les différents cas.

    def CardsICanPlay(self , bidcolor, pli,MyHand):   
        if len(pli)==0 :                                                # si le pli est vide le joeuur joue en premier, il peux jouer n'importe laquelle de ses cartes
            return(range(0,len(MyHand)))   
        else:
            ColAsked = pli[0].color
            if ColAsked == bidcolor :                                   # si la couleur demandée (jouer par le premier joueur du pli) est l'atout
                MaxTrumpPlayed = -1                                     # On cherche la force de l'atout le plus fort joué
                for c in pli : 
                    if c.color == bidcolor and STRENGH_ATOUTS[c.value]>MaxTrumpPlayed :
                        MaxTrumpPlayed = STRENGH_ATOUTS[c.value]
                ImigthPlay = []                                        # cartes atout de la main du jouer
                IcanPlay = []                                          # carte atout de force plus élevée que toutes les cartes atouts jouées
                for i in range(len(MyHand)):
                    if MyHand[i].color == ColAsked:
                        ImigthPlay.append(i)
                        if STRENGH_ATOUTS[MyHand[i].value] > MaxTrumpPlayed :
                            IcanPlay.append(i)
                if len(IcanPlay) != 0 :                                # Si le joueur peux monter à l'atout il doit le faire
                    return(IcanPlay)
                else :                                                 # sinon s'il a des atouts il doit quand même jouer atout
                    if len(ImigthPlay) == 0:                
                        return(range(0,len(MyHand)))                   # et s'il n'a pas d'atout dutout alors il doit pisser, il peux jouer n'improte qu'elle carte de son jeu
                    else : 
                        return(ImigthPlay)
            else :                                                     # Si la couleur demandée n'est pas l'atout
                ICanPlay = []                                          # Toutes ses cartes de la couleur demandée
                for i in range (len(MyHand)):
                    if MyHand[i].color == ColAsked : 
                        ICanPlay.append(i)
                if len(ICanPlay) != 0:                                 # S'il a des cartes de la couleurs demandée alors jil doit les jouer
                    return(ICanPlay)
                else :                                                 # sinon
                    MyTrumpCard = []
                    for i in range (len(MyHand)):
                        if MyHand[i].color == bidcolor : 
                            MyTrumpCard.append(i)
                    if len(MyTrumpCard) == 0 :                         # s'il n'a pas d'atout il pisse, il peut jouer n'importe qu'elle carte de sa main              
                        return(range(0,len(MyHand)))
                    else :                                             # sinon alors la c'est la galère il y plein de cas
                        MaxTrumpPlayed = -10
                        for c in pli : 
                            if c.color == bidcolor and STRENGH_ATOUTS[c.value]>MaxTrumpPlayed:
                                MaxTrumpPlayed = STRENGH_ATOUTS[c.value]
                        if MaxTrumpPlayed == -10 :                                                  # si personne n'a joué d'atout
                            if len(pli)==1 :                                                        # si son partenaire n'a pas encore joué
                                return(MyTrumpCard)                                                 # forcement il n'est pas maitre donc le joueur est obligé de jouer atout
                            else :                                                                  # si il a joué
                                myPartner = len(pli)-2                                              # alors voila la position de sa carte dans le plis
                                myPartnerIsTheBest = True                                           # on regarde s'il gagne le pli pour le moment
                                for i in range (len(pli)):              
                                    if i != myPartner : 
                                        if STRENGH[pli[myPartner].value]< STRENGH[pli[i].value]:
                                            myPartnerIsTheBest = False
                                            break
                                if myPartnerIsTheBest :                                             # si pour le moment il gagne le plis
                                    return(range(0,len(MyHand)))                                    # le joueur peut jouer nimporte laquelle de ses cartes   
                                else : 
                                    return(MyTrumpCard)                                             # sinon il est obligé de jouer atout
                                    
                        else :                                                                      # si un atout à été joué 
                            MyTrumpCardBetterThanPlayed = []
                            for cardpos in MyTrumpCard : 
                                if STRENGH_ATOUTS[MyHand[carpos].value] > MaxTrumpPlayed : 
                                    MyTrumpCardBetterThanPlayed.append(cardpos)
                            if len(MyTrumpCardBetterThanPlayed) == 0 :                              # si le joueur n'a pas de carte atout superieure à celle jouée il peut jouer n'importe laquelle
                                return(myTrumpCard)     
                            else :                                                                  # sinon il est obligé de monter à l'atout
                                return(MyTrumpCardBetterThanPlayed)

#Incrémentation d'une variable de façon à "tourner autour de la table dans le sens des aiguilles d'une montre"

    def Next(self,player):
        return((player+1)%NBR_PLAYER)


#Permet de savoir ce qui nous a fait sortir du tant que et qui met fin à la partie, autrement dit qui a gagné
    def WhoWonTheGame(self) :
        Winner = None
        if self.teamGamePoints[0]>POINTSGAME :
            Winner = 0
            if self.teamGamePoints[1]>POINTSGAME : # Si les deux équipes dépassent POINTSGAME à la fin du même round alors elles ont toute les deux gagné
                Winner = 2
        elif self.teamGamePoints[1]>POINTSGAME :
            Winner = 1
        return(Winner)

                            #############################################################################
                            ############################ Méthodes logique réseau ########################
                            #############################################################################
                            
# Dans l'idée de séparer un maximum la logique réseau de la logique jeu (dans l'optique d'éventuellement passer un jour à une interface graphique) nous avons créer des
# méthodes à chaque fois qu'on voulait transmettre une information à tous les joueurs. Chaque événement à un tag correspondant appelé command, on envoie au client 
# des information sous le forme COMMAND + SEP + INFO1 + INFO2 ect.... Le client traite l'information selon la COMMAND



#Methode permettant de vérifier coté serveur que l'information a bien été reçu par le client et que la réponse est adaptée si toute fois une réponse est attendue
    def receivedFromPlayer(self,command,playerIndice):
        rcv = self.listeClient[playerIndice].recv(TAILLE_BLOC)
        rcv = rcv.split(SEP)
        while rcv[0]!= command :
            rcv = self.listeClient[playerIndice].recv(TAILLE_BLOC)
            rcv = rcv.split(SEP)
        return(rcv)

#En début de partie on informe les joueurs de la position à laquelle ils jouent 
    def SendTheirPosToPlayer(self) :
        for i in range (NBR_PLAYER):                                            
            self.listeClient[i].send(GIVENUMBER+SEP+str(i))                     
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)                     
            

# A chaque fois que les points d'une équipe changent, c'est à dire à chaque fin de round, on en informe les joueurs pour qu'il mettent à jour leur interface graphique
    def SendTheirTeamPointsToPLayer(self) : 
        for i in range (NBR_PLAYER):
            self.listeClient[i].send(TEAMPOINTS + SEP + str(self.teamGamePoints[0])+ SEP + str(self.teamGamePoints[1]))                     
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i) 

# Informe le client qu'un jeu (enchère + round) va commencer (MAJ interface graphique)
    def InformClientsNewGameStart(self): 
        for i in range (NBR_PLAYER):                                            
            self.listeClient[i].send(STARTNEWPHASE+ SEP + GAME+SEP+str(i))                      
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)  

# Informe le client qu'une des enchère vont commencer (MAJ interface graphique). Il a besoin de savoir qui parle pour afficher les enchères sous les bons joueurs
    def InformClientsBidStart(self,speaker):
        for i in range (NBR_PLAYER):
            self.listeClient[i].send(STARTNEWPHASE + SEP + BIDSTART + SEP + str(speaker))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)

# Au début de chaque jeu (enchère + round) après avoir distribué les cartes ont transmet à chaque joueur sa main (carte par carte)
    def sendTheirHandToPlayers(self):
        for i in range (NBR_PLAYER):   
            for j in range (8):
                self.listeClient[i].send(ACARDOFYOURHAND+SEP+str(self.hands[i][j]))                    
                NoAnwerCheck = self.receivedFromPlayer(CHECK,i)    

# A la fin des enchères on informe les clients de l'enchère retenue 
    def InformClientsFinalBid(self,bidRes):
        for i in range (NBR_PLAYER):                    
            self.listeClient[i].send(STARTNEWPHASE + SEP + ROUNDSTART +  SEP + TEAMS[bidRes.team] + SEP + bidding_to_string(bidRes.bid))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)


# A la fin d'un pli on informe les client du gagnant (pour afficher ensuite les cartes sous les bon joueur puisque le gagant du pli n-1 commence au pli n)
    def informClientsPliWinner(self,PliWinner):
        for i in range (NBR_PLAYER):
            self.listeClient[i].send(ENDPLI + SEP + PliWinner)
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)


# Informe les clients de celui qui doit jouer. 
    def InformClientCurrentPlayer(self,currentPlayer): 
        for j in range(NBR_PLAYER): 
            self.listeClient[j].send(CURRENTPLAYING + SEP + str(currentPlayer))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,j)

# Informe les clients de celui qui est en train de faire l'enchère.
    def InformClientsCurrentBidder(self, speaker):
        for i in range(NBR_PLAYER): 
            self.listeClient[i].send(CURRENTBIDDING + SEP + str(speaker))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)
        
# Informe les clients qu'une carte a été jouée et par quel joueur. 
    def InformPlayerACardWasPlaced(self, currentPlayer,CardPlace):
        for j in range(NBR_PLAYER): 
            self.listeClient[j].send(CARDWASPLAYED + SEP + str(self.hands[currentPlayer][int(CardPlace)]) + SEP + str(currentPlayer))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,j)

# A chaque fois qu'un enchère est faite (ou un passe) on le transmet aux clients pour affichage
    def UpdatePlayersGraphBid(self,postochange,changing) :
        for i in range (NBR_PLAYER) : 
            self.listeClient[i].send(UPDATEBID + SEP + str(postochange) + SEP + str(changing))
            NoAnwerCheck = self.receivedFromPlayer(CHECK,i)
        
