# -*- coding: utf-8 -*-
import random
from card import Card
from global_values import*
from math import *

# Jeu de 32 cartes

class Deck():
    # Initialisation du jeu de 32 cartes (de 7 à As, de trèfle à coeur)
    def __init__(self):
        self.card_list=[Card(i,j) for i in range(8) for j in range(4)]  


    # Mélange le jeu
    def shuffle(self):
        random.shuffle(self.card_list)


    # Distribue le jeu aux 4 joueurs
    # Les cartes seront distribuées 3 par 3, puis 2 par 2, puis 3 par 3
    def distribute_deck(self):
        scheme = [3,2,3]
        lots = [[] for i in range(4)]
        for card_number in scheme :
            for lot_number in range(4) : 
                lots[lot_number].extend(self.card_list[0:card_number])
                self.card_list=self.card_list[card_number:]
        for i in range (len(lots)):
            lots[i] = self.order_cards(lots[i])
        return lots


    # Reforme le deck à partir de plusieurs tas
    # utilisés à la fin d'un round
    def stackToDeck(self,lots):
        self.card_list = []	
        for lot in lots :
            for card in lot : 
                self.card_list.append(card)
        coupe = random.randint(1,31)
        self.card_list = self.card_list[coupe:]+self.card_list[:coupe]


    # Trie les cartes d'une main par couleur et par valeur croissante
    # Utilisé au moment où les cartes sont distribuées
    def order_cards(self,cardList):
        color_ordered = [[] for i in range(4)]
        for card in cardList:
            color_ordered[card.color].append(card)
        for p in range (len(color_ordered)):
            color = color_ordered[p]
            size = len(color)
            for i in range (int((size%2)+floor(size/2))):
                min = color[i]
                max = color[i]
                for j in range (i,size-i):
                    if color[j].value>max.value :
                        max = color[j]
                    if color[j].value<min.value :
                        min = color[j]
                color.remove(max)
                color.insert(size - i - 1,max)
                if max != min : 
                    color.remove(min)
                    color.insert(i,min)
            color_ordered[p]=color
        return(color_ordered[0]+color_ordered[1]+color_ordered[2]+color_ordered[3])
            

