						      oooooooooooooooooooooooooooo
						      o JEU DE COINCHE EN RESEAU o
						      oooooooooooooooooooooooooooo

La coinche est un jeu qui se joue avec 32 cartes par équipe de 2 joueurs. Le but est de remplir un contrat défini à chaque round au cours des enchères.
Les équipes N/S et E/O s'affrontent. 
Vous trouverez les règles détaillées de la coinche à cette adresse : https://www.belote.com/regles-et-variantes/regle-belote-coinche/



							===== INSTALLATION =====
Ce  programme recquiert Python 2.7 pour fonctionner.
Les librairies time, socket, os et random sont nécessaire au bon fonctionnenment du programme.



					         ===== COMMENT LANCER UNE PARTIE =====
Il est nécessaire d'être 4 joueurs pour lancer une partie.
Il faut vérifier dans le fichier global_values.py que l'adresse indiquée dans la variable host soit bien celle du joueur hébergeur.
Le premier joueur (hébergeur) doit lancer le script serveur.py, puis tous les joueurs peuvent lancer le script client.py.



						 ===== DEROULEMENT D'UNE PARTIE =====
Une fois les 4 joueurs connectés, la partie peut commencer.
Le jeu consiste en une succession de rounds jusqu'a ce que l'une des 2 équipes (N/S ou E/O) remporte 2000 points. 
Chaque round est composé d'une session d'enchères, puis d'une session de jeu (8 plis).
C'est le joueur N qui commence à distribuer.
	==> ENCHERES
Au début des enchères, les cartes sont distribuées aux 4 joueurs. A tour de rôle, les 4 joueurs vont avoir la possibilité de faire une enchère ou de passer (écrire 0 ou 1). 
C'est le joueur à gauche du joueur qui a distribué qui commence les enchères.
S'il choisit de faire un enchère, il doit commencer par choisir la valeur (de 80 à capot en écrivant la position de 0 à 9). Ensuite il peut choisir la couleur du contrat (0 à 3).
Les enchères se terminent une fois que trois joueurs d'affilé passent.
	==> JEU
A chaque pli, le joueur ayant remporté le pli précédant (ou le joueur ayant commencé les enchères) commence à jouer.
Chaque joueur choisit la carte qu'il veut jouer en indiquant sa position (0 à 7).



                                                 ===== CHANGEMENT DES PARAMETRES =====
Il est possible de changer certains paramètres dans le fichier global_values.py. 
Il est possible de changer la variable pointsGame qui définit le nombre de points à atteindre pour remporter la partie. Cela permet de gérer la durée d'une partie !!!

        ==>Conseils :
Afin de tester rapidement le programme vous pouvez commenter le sleep à la fin de chaque pli (ligne 84)