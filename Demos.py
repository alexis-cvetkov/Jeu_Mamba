#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:47:01 2019

@author: alexis
"""

import ControleurJeu
import InterfaceJeu

# =============================================================================
#                   Start the game in graphical mode
# =============================================================================

# Snake controls if Human -> Z, Q, S, D (on azerty keyboard)
# Monster controls if Human -> I, J, K, L, H
# Pause -> P key
# End game -> Esc. key

snake_AI = 'Human' # Human, Random, Intermediate
monster_AI = 'Human' # Human, Random, Intermediate, Advanced

snake_speed = 1
monster_speed = 1

cell_size = 10 # Size in pixels of every grid cell
grid_shape = (50,100) # Number of rows, columns

params = params_jeu(taille_terrain=grid_shape, taille_case=cell_size,
                    IA_monstre=monster_AI, IA_serpent=snake_AI,
                    vitesse_serpent=snake_speed, vitesse_monstre=monster_speed)

# --- A decommenter pour lancer le jeu en mode graphique
jeu = ControleurJeu.ControleurJeu(params)


# =============================================================================
#               Parameters configuration with the menu (NOT WORKING YET)
# =============================================================================

#app = QApplication(sys.argv)
#interface = InterfaceJeu.InterfaceJeu()
#interface.show()
#app.exec()
#
#params = interface.menu.params.get_params()
#print(params)































