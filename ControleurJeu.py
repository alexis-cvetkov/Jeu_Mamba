#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 21:43:20 2019

@author: alexis
"""

import numpy as np
import sys
from random import (random, choice)
from skimage.draw import polygon
from ModeleJeu import *
import InterfaceJeu
from Tools import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ControleurJeu():
    
    def __init__(self,params):
        
        """
        Crée une instance de la classe ControleurJeu.
        
        Paramètres
        ----------
        
        params : dict
            L'ensemble des paramètres configurables du jeu (taille de la carte,
            IA et vitesses des personnages, ...).
            
        Attributs
        ---------
        
        terrain : Terrain
            Instance de la classe Terrain. Contient une matrice décrivant l'état
            du terrain et la position des joueurs.
        serpent : Serpent
            Instance de la classe Serpent.
        monstre : Monstre
            Instance de la classe Monstre.
        pause : int
            Un entier décrivant l'état du jeu. 1 quand le jeu est en pause,
            0 sinon.
            
        interface : str
            interface = 'Graphique' ou 'Console' selon les paramètres du jeu.
        fenetre : FenetreJeu
            La fenetre de jeu en mode graphique.
        timer_serpent : QTimer
            Le timer associé à l'éxécution d'un tour du serpent.
            Toutes les T1 millisecondes, la méthode update_serpent est lancée.
        timer_monstre : QTimer
            Le timer associé à l'éxécution d'un tour du serpent.
            Toutes les T2 millisecondes, la méthode update_monstre est lancée.   

        """
        
        # --- Initialisation du Terrain, du Serpent et du Monstre        
        self.terrain = Terrain(params)
        self.serpent = Serpent(params)
        self.monstre = Monstre(params)
        self.pause = 0
        
        # --- Initialisation de la fenetre et des timers en mode graphique
        self.interface = params['interface']
        if self.interface == "Graphique":
            
            vs,vm = params["vitesse_serpent"],params["vitesse_monstre"]
            nl,nc = params["taille_terrain"]
            
            app = QApplication(sys.argv)
            self.fenetre = InterfaceJeu.FenetreJeu(params,self)
            self.timer_serpent = QTimer()
            self.timer_serpent.timeout.connect(self.update_serpent)
            self.timer_serpent.start(int(5000/(vs*nc)))
            self.timer_monstre = QTimer()
            self.timer_monstre.timeout.connect(self.update_monstre)
            self.timer_monstre.start(int(5000/(vm*nc)))
            self.fenetre.show()
            app.exec()
        
    # =========================================================================
    #                 Méthodes associées au contrôle du Serpent
    # =========================================================================
    
    def deplace_serpent(self):
        
        """
        Actualise la position du Serpent lors de son déplacement, la valeur de
        son compteur s'il change de zone ainsi que terrain.joueurs.
        
        """
        
        serpent = self.serpent
        terrain = self.terrain
        map_joueurs = terrain.joueurs
        map_zones = terrain.zones
        
        # --- Ancienne position du Serpent
        l,c = old_position = serpent.position 
        dl,dc = serpent.direction
        nl,nc = terrain.size # taille de la carte
    
        # --- Nouvelle position du Serpent
        new_position = (l+dl)%nl,(c+dc)%nc
        serpent.position = new_position
        
        # --- Incrémentation de self.cpt        
        old_zone,new_zone = map_zones[old_position],map_zones[new_position]
        if  old_zone != new_zone : # changement de zone
            serpent.cpt += 1
            if serpent.cpt == 1:
                serpent.depart = old_position    
            else:
                serpent.arrivee = new_position
        
        # --- Modification de map_joueurs
        if old_zone: # le Serpent se trouvait déjà dans la zone du Monstre
            map_joueurs[old_position] = -1    
            serpent.corps.append(old_position)
        else: # le Serpent se trouvait dans sa zone
            map_joueurs[old_position] = 0
            
        map_joueurs[new_position] = 1
        return        
        
    def update_serpent(self,direction=None):
        
        if self.interface == 'Graphique':
            self.key_event()
        
        if self.pause:
            return
        
        self.change_direction_serpent(direction)
        self.deplace_serpent()
        self.test_collision()
        if self.interface == 'Graphique':
            terrain = self.terrain
            serpent = self.serpent
            self.fenetre.carte.dessin.redessine(terrain,serpent,'Serpent')
        if self.serpent.cpt == 2: # On rentre à nouveau dans la zone safe donc on grise la zone dessinée.
            corps, rr, cc = self.grise_zone()
            if self.interface == 'Graphique':
                self.fenetre.carte.dessin.grise_dessin(corps,rr,cc)
            self.serpent.cpt = 0            
        return
    
    def directions_possibles_serpent(self):
        
        """
        Renvoie la liste des directions possibles que peut prendre le Serpent
        à un instant donné.
        
        """
        
        terrain = self.terrain
        serpent = self.serpent
        
        # --- Position et direction actuelle du joueur
        l,c = serpent.position
        dl,dc = serpent.direction
        nl,nc = terrain.size
        
        # --- Creation de la liste des directions possibles
        D = [(1,0),(-1,0),(0,1),(0,-1)]
        D.remove((-dl,-dc))
        directions_possibles = D.copy()
        
        # --- On retire les directions menant au corps du serpent
        if serpent.IA != 'Human':
            for direction in D:
                dl,dc = direction
                new_position = (l+dl)%nl,(c+dc)%nc
                if terrain.joueurs[new_position] == -1:
                    directions_possibles.remove(direction)
        
        return directions_possibles
    
    def change_direction_serpent(self,direction=None):
        
        """
        Change la direction du serpent en fonction du type du joueur qui le
        contrôle (Human ou IA plus ou moins complexe).
        
        IA = Human: on change manuellement la direction du serpent
        avec le paramètre direction.
        
        IA = Aléatoire: le serpent change aléatoirement de direction avec
        une certaine probabilité (ou lorsque sa direction actuelle n'est pas
        possible).
        
        IA = Intermédiaire: comportement aléatoire tant que le serpent.
        
        """
        
        terrain = self.terrain
        serpent = self.serpent
        monstre = self.monstre
        IA = serpent.IA
        map_zones = terrain.zones
        position = serpent.position
        directions_possibles = self.directions_possibles_serpent()
        
        # --- Si le joueur est Human on change manuellement sa direction
        if IA == 'Human':
            if direction in directions_possibles:
                serpent.direction = direction
            else:
                return
        
        # --- IA qui change aléatoirement de direction avec une proba 0.05
        # ou lorsque le Serpent n'a pas d'alternatives
        elif IA == 'Random' :
            if (random() > 0.90) or (serpent.direction not in directions_possibles):
                direction = choice(directions_possibles)
                serpent.direction = direction 
        
        # --- IA intermédiaire qui se déplace aléatoire dans sa zone . Quand
        # elle entre dans la zone du monstre elle trouve un chemin vers sa zone
        # assez court pour ne pas se faire manger par le monstre
        elif IA == 'Intermediate' :
            if map_zones[position] == 0:
                serpent.IA = 'Random'
                self.change_direction_serpent()
                serpent.IA = 'Intermediate'
            else:
                if serpent.direction_list == []:
                    dist = path_finding(map_zones,position,[monstre.position],
                                        zone_autorisee=1,output='length')
                    n_coups = max(dist//2 - 1,3)
                    serpent.direction_list = path_finding_max(terrain,position,
                                                              0, n_coups)
                    #print(serpent.direction_list)
                if serpent.direction_list is None:
                    serpent.IA = 'Random'
                    self.change_direction_serpent()
                    serpent.IA = 'Intermediate'
                else:
                    serpent.direction = serpent.direction_list.pop(0)

        return 
    
    def grise_zone(self):
        
        """
        Grise la zone capturée par le Serpent.
        Délimite un contour de la zone à griser puis remplis le polygone ainsi
        défini.
        
        Retourne
        --------
        
        corps : list
            La liste des coordonées des cases appartenant au corps du serpent.
        rr : numpy.ndarray
            Vecteur contenant l'indice (en ligne) des points à griser.
        cc : numpy.ndarray
            Vecteur contenant l'indice (en colonne) des points à griser.
            
        """
        
        map_zones = self.terrain.zones
        map_joueurs = self.terrain.joueurs
        depart = [self.serpent.depart]
        arrivee = self.serpent.arrivee
        corps = self.serpent.corps
        zone_autorisee = 0
        
        # Plus court chemin reliant les extrémités de la boucle du serpent
        path = path_finding(map_zones,arrivee,depart,zone_autorisee,output='path')                
        contour = path + corps # L'ordre des points est important pour delimiter le polygone correctement.
        
        for point in corps:
            map_zones[point] = 0
            
        poly = np.array(contour)
        rr,cc = polygon(poly[:,0],poly[:,1],map_zones.shape)
        map_zones[rr,cc] = 0
        
        # --- On reset le corps du serpent et map_joueurs
        for point in corps:
            map_joueurs[point] = 0
        self.serpent.corps = []
        
        return corps,rr,cc
    
    # =========================================================================
    #                 Méthodes associées au contrôle du Monstre
    # =========================================================================
    
    def deplace_monstre(self):
        
        """
        Actualise la position du Monstre lors de son déplacement ainsi que
        terrain.joueurs.
        
        """
        
        monstre = self.monstre
        map_joueurs = self.terrain.joueurs
        
        # --- Test si le Monstre est immobile
        if monstre.direction == (0,0):
            return
        
        # --- Ancienne position du Monstre
        l,c = old_position = monstre.position
        dl,dc = monstre.direction
    
        # --- Nouvelle position du Monstre
        new_position = l+dl,c+dc
        monstre.position = new_position
        
        # --- Modification de map_joueurs
        map_joueurs[old_position] = 0
        map_joueurs[new_position] = 2
    
        return
     
    def update_monstre(self,direction=None):
        
        if self.pause:
            return
        if self.interface == 'Graphique':
            self.key_event()
            
        self.change_direction_monstre(direction)
        self.deplace_monstre()
        if self.interface == 'Graphique':
            terrain = self.terrain
            monstre = self.monstre
            self.fenetre.carte.dessin.redessine(terrain,monstre,'Monstre')
        self.test_collision()
        return
        
    
    def directions_possibles_monstre(self):
        
        terrain = self.terrain
        monstre = self.monstre
        
        # --- Position et direction actuelle du joueur
        l,c = monstre.position
        dl,dc = monstre.direction
        nl,nc = terrain.size
        
        # --- Creation de la liste des directions possibles
        D = [(1,0),(-1,0),(0,1),(0,-1)]
        directions_possibles = D.copy()
        
        # --- On enlève les directions menant dans la zone du Serpent
        for direction in D:
            dl,dc = direction
            new_position = (l+dl)%nl,(c+dc)%nc
            if terrain.zones[new_position] == 0:
                directions_possibles.remove(direction)
        directions_possibles.append((0,0))
        
        return directions_possibles
    
    def change_direction_monstre(self,direction=None):
        
        """
        Change la direction du monstre en fonction du type du joueur qui le
        contrôle (Human ou IA plus ou moins complexe).
        
        IA = Human: on change manuellement la direction du monstre
        avec le paramètre direction.
        
        IA = Aléatoire: le monstre change aléatoirement de direction avec
        une certaine probabilité (ou lorsque sa direction actuelle n'est pas
        possible).
        
        IA = Intermédiaire: comportement aléatoire tant que le serpent est dans
        sa zone. Quand il rentre dans la zone du monstre ce dernier suit le 
        chemin le plus court vers le serpent.
        
        IA = Avancée: Idem que Intermédiaire mais quand le serpent est dans sa
        zone le monstre se dirige vers le point le plus proche du serpent mais
        qui reste dans la zone du monstre.
        
        """
        
        terrain = self.terrain
        serpent = self.serpent
        monstre = self.monstre        
        IA = monstre.IA
        map_zones = terrain.zones
        position = monstre.position
        directions_possibles = self.directions_possibles_monstre()

        # --- Cas où le Personnage est Human
        if IA == 'Human':
            if direction in directions_possibles:
                monstre.direction = direction
            elif monstre.direction in directions_possibles:
                return
            else:
                monstre.direction = (0,0)
        
        # --- IA qui change aléatoirement de direction avec une proba 0.05
        # ou lorsque le monstre n'a pas d'alternatives
        if IA == 'Random' :
            if (random() > 0.9) or (monstre.direction not in directions_possibles):
                directions_possibles.remove((0,0))
                if directions_possibles != []:
                    direction = choice(directions_possibles)
                else:
                    direction = (0,0)
                monstre.direction = direction    
                
        # --- IA intermédiaire qui fonce sur le serpent lorsqu'il est dans la
        # zone du monstre et qui est aléatoire sinon
        elif IA == 'Intermediate' :        
            if map_zones[serpent.position] == 1:
                direction = path_finding(map_zones,position,serpent.corps+[serpent.position],1,output='direction')
                monstre.direction = direction                            
            else:
                self.monstre.IA = 'Random'
                self.change_direction_monstre()
                self.monstre.IA = 'Intermediate'
        
        # --- IA avancée qui ajoute à l'IA intermédiaire la capacité de suivre
        # le serpent même lorsqu'il est dans sa zone
        elif IA == 'Advanced':            
            if map_zones[serpent.position] == 1:
                direction = path_finding(map_zones,position,serpent.corps+[serpent.position],1,output='direction')
                monstre.direction = direction                            
            else:
                serpent_virtuel = path_finding_zone(map_zones,serpent.position,
                                                    zone_arrivee=1,output='arrivee')
                direction = path_finding(map_zones,position,serpent_virtuel,
                                         zone_autorisee=1,output='direction')
                monstre.direction = direction
        return
    
    # =========================================================================
    #                           Méthodes auxiliaires
    # =========================================================================
        
    def test_collision(self):
        
        """ Vérification des collisions serpent-serpent et serpent-monstre. """
        
        serpent = self.serpent
        monstre = self.monstre
        map_zones = self.terrain.zones
        nl, nc = map_zones.shape
        
        # --- Collision du serpent avec lui même
        if serpent.position in serpent.corps:
            print('GAME ENDS')
            print('Coverage of the captured area: {}'.format(
                    1-map_zones.sum()/(0.8*nc*(nl-0.2*nc))))
            if self.interface == 'Graphique':
                self.pause = 1 - self.pause
                
        # --- Collision du serpent avec le monstre
        elif monstre.position in serpent.corps:
            print('GAME ENDS')
            print('Coverage of the captured area: {}'.format(
                    1-map_zones.sum()/(0.8*nc*(nl-0.2*nc))))
            if self.interface == 'Graphique':
                self.pause = 1 - self.pause
        return
    
    def key_event(self):
        
        """
        Lecture des attributs de self.fenetre et exécution des actions
        associées (changement de direction, mise en pause).
        
        """
        
        key_serpent = self.fenetre.key_serpent
        key_monstre = self.fenetre.key_monstre
        key_annexe = self.fenetre.key_annexe
        
        direction_serpent = None
        direction_monstre = None
        self.fenetre.key_serpent = None
        self.fenetre.key_monstre = None
        self.fenetre.key_annexe = None
        
        if key_annexe == Qt.Key_Escape:
                self.fenetre.close()
            
        elif key_annexe == Qt.Key_P: # On passe le jeu en pause / continue
            self.pause = 1 - self.pause
        
        if not self.pause and self.serpent.IA == 'Human':
            if key_serpent == Qt.Key_Z:
                direction_serpent = (-1,0) 
            elif key_serpent == Qt.Key_D:
                direction_serpent = (0,1)
            elif key_serpent == Qt.Key_S:
                direction_serpent = (1,0)
            elif key_serpent == Qt.Key_Q:
                direction_serpent = (0,-1)
            
        if not self.pause and self.monstre.IA == 'Human':
            if key_monstre == Qt.Key_I:
                direction_monstre = (-1,0) 
            elif key_monstre == Qt.Key_L:
                direction_monstre = (0,1)
            elif key_monstre == Qt.Key_K:
                direction_monstre = (1,0)
            elif key_monstre == Qt.Key_J:
                direction_monstre = (0,-1)
            elif key_monstre == Qt.Key_H:
                direction_monstre = (0,0)
        
        if self.serpent.IA == 'Human':
            self.change_direction_serpent(direction_serpent)
        if self.monstre.IA == 'Human':
            self.change_direction_monstre(direction_monstre)
        return
