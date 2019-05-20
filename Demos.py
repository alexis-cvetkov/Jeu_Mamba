#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:47:01 2019

@author: alexis
"""

import ControleurJeu
import InterfaceJeu
from Tools import *

def affiche_terrain(terrain):
    
        # --- Affiche la carte des zones
        print('_________________________________________\n')
        print('CARTE DES ZONES\n')
        for case in terrain.zones:
            print(*case, sep=" ")
        
        # --- Affiche la carte des joueurs
        print('_________________________________________\n')
        print('CARTE DES JOUEURS\n')
        for case in terrain.joueurs:
            print(*case, sep=" ")
            
            
# =============================================================================
#                     Lancement d'une partie en mode Console
# =============================================================================


params = params_jeu(taille_terrain=(10,10),IA_monstre='Humain',
                    interface='Console')

jeu = ControleurJeu.ControleurJeu(params)
terrain = jeu.terrain
serpent = jeu.serpent
monstre = jeu.monstre

affiche_terrain(terrain)

jeu.update_serpent(direction=(0,1))
jeu.update_serpent(direction=(0,1))
jeu.update_serpent(direction=(0,1))

jeu.update_serpent(direction=(1,0))
jeu.update_serpent(direction=(1,0))
jeu.update_serpent(direction=(1,0))

jeu.update_serpent(direction=(0,-1))
jeu.update_serpent(direction=(0,-1))
#jeu.update_serpent(direction=(0,-1))

#jeu.update_monstre(direction=(0,-1))
#jeu.update_monstre(direction=(-1,0))

affiche_terrain(terrain)


# =============================================================================
#                   Lancement d'une partie en mode Graphique
# =============================================================================

# Deplacement du Serpent en mode Humain -> touches Z,Q,S,D
# Deplacement du Monstre en mode Humain -> touches I,J,K,L,H
# Pause -> touche P
# Fermer le jeu -> Touche Echap

IA_monstre = 'Avancée' # Humain, Aléatoire, Intermédiaire, Avancée
IA_serpent = 'Humain' # Humain, Aléatoire, Intermédiaire
params = params_jeu(taille_terrain=(50,100),IA_monstre=IA_monstre,
                    IA_serpent=IA_serpent,vitesse_serpent=1,vitesse_monstre=1)

# --- A decommenter pour lancer le jeu en mode graphique
jeu = ControleurJeu.ControleurJeu(params)


# =============================================================================
#               Configuration des paramètres de jeu avec le menu
# =============================================================================

# --- Non fonctionnel pour l'instant
#app = QApplication(sys.argv)
#interface = InterfaceJeu.InterfaceJeu()
#interface.show()
#app.exec()
#
#params = interface.menu.params.get_params()
#print(params)































