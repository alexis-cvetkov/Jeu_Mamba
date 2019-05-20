#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 21:43:20 2019

@author: alexis
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def params_jeu(**params):
    
    """
    Fonction retournant un dictionnaire contenant tout les paramètres
    du jeu.
    
    Paramètres
    ----------
    
    params : dict
        L'ensemble des paramètres du jeu dont on souhaite modifier la valeur
        par défaut.
        
    Retourne
    --------
    
    param_dict = {}
        Dictionnaire contenant les paramètres du jeu. Les paramètres ont une
        valeur par défaut que l'on peut réecrire avec params.
    
    """
    
    param_dict = {}
    
    # --- Taille de la carte et des cases
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    w = screen_resolution.width()
    h = screen_resolution.height()
    param_dict["taille_case"] = px = 10 # px
    param_dict["taille_terrain"] = nl,nc = int(0.8*h/px),int(0.8*w/px)
    
    # --- IA des personnages
    param_dict["IA_serpent"] = 'Humain'
    param_dict["IA_monstre"] = 'Humain'
    
    # --- Vitesses des personnages
    param_dict["vitesse_serpent"] = 1
    param_dict["vitesse_monstre"] = 1
    
    param_dict["interface"] = "Graphique"
    param_dict.update(params)
    
    return param_dict

def path_finding(map_zones,depart,arrivee,zone_autorisee,output='path'):
    
    """
    Trouve le plus court chemin entre une position et un ensemble de positions.
    Utilise un algorithme de type BFS (Breadth First Search).
    
    Paramètres
    ----------
    
    map_zones : numpy.ndarray
        La matrice des zones du terrain.
    depart : tuple
        Les coordonnées (ligne,colonne) du point de départ.
    arrivee : list
        L'ensemble des positions des points à rejoindre.
    zone_autorisee : int
        Le type des cases que l'on peut explorer pour trovuer le plus court
        chemin. 0 (resp. 1) pour forcer le passage à travers la zone du
        serpent (resp. du monstre).
    output : str
        Format des données en sortie de la fonction.
    
    """
    
    path_list = [[depart]]
    seen_positions = set([depart])
    nl,nc = map_zones.shape
    
    while path_list: # Tant que path_list n'est pas vide
        
        # --- Récupère la dernière position du chemin exploré le plus court
        path = path_list.pop(0)
        x,y = path[-1]
        
        # --- Renvoie le chemin s'il atteint l'arrivée
        if (x,y) in arrivee:
            return reformat(path,output)
        
        # --- Crée 4 chemins à partir des voisins du chemin précédent
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
            if 0 <= x2 < nl and 0 <= y2 < nc and map_zones[x2][y2] == zone_autorisee \
            and (x2, y2) not in seen_positions:
                path_list.append(path + [(x2, y2)])
                seen_positions.add((x2, y2))
    
    # --- Si aucun chemin n'est trouvé, on reste sur place.
    return reformat([depart],output)

def path_finding_zone(map_zones,depart,zone_arrivee,output='path'):
    
    """
    Trouve le plus court chemin entre une position et une zone.
    Utilise un algorithme de type BFS (Breadth First Search).
    
    Paramètres
    ----------
    
    map_zones : numpy.ndarray
        La matrice des zones du terrain.
    depart : tuple
        Les coordonnées (ligne,colonne) du point de départ.
    zone_arrivee : int
        Le type de zone d'arrivée, zone_arrivee = 1 (resp.) 0 pour la zone du 
        monstre (resp. du serpent).
    output : str
        Format des données en sortie de la fonction.
    
    """
    
    path_list = [[depart]]
    seen_positions = set([depart])
    nl,nc = map_zones.shape
    
    while path_list: # Tant que path_list n'est pas vide
        
        # --- Récupère la dernière position du chemin exploré le plus court
        path = path_list.pop(0)
        x,y = path[-1]
        
        # --- Renvoie le chemin s'il atteint l'arrivée
        if map_zones[x,y] == zone_arrivee:
            return reformat(path,output)
        
        # --- Crée 4 chemins à partir des voisins du chemin précédent
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
            if (x2,y2) not in seen_positions and 0 <= x2 < nl and 0 <= y2 < nc:
                path_list.append(path + [(x2, y2)])
                seen_positions.add((x2, y2))

def path_finding_max(terrain,depart,zone_arrivee,n_coups):
    
    """
    Trouve le plus long chemin de moins de n coups vers une zone d'arrivée.
    Utilise un algorithme de type BFS (Breadth First Search).
    
    Paramètres
    ----------
    
    terrain : Terrain
        Une instance du Terrain de jeu.
    depart : tuple
        Les coordonnées (ligne,colonne) du point de départ.
    zone_arrivee : int
        Le type de zone d'arrivée, zone_arrivee = 1 (resp.) 0 pour la zone du 
        monstre (resp. du serpent).
    n_coups : int
        Le longueur maximale des chemins vers la zone d'arrivée.
    
    """
    map_zones = terrain.zones
    map_joueurs = terrain.joueurs
    
    path_list = [[depart]]
    seen_positions = set([depart])
    nl,nc = map_zones.shape
    path_saved = []
    while path_list: # Tant que path_list n'est pas vide
        
        # --- Récupère la dernière position du chemin exploré le plus court
        path = path_list.pop(0)
        x,y = path[-1]
        
        # --- Si les nouveaux chemins sont trop longs on arrete d'explorer
        if len(path) > n_coups:
            return reformat(path_saved[-1],output='directions')
        
        # --- Ajoute le chemin s'il atteint l'arrivée
        if map_zones[x,y] == zone_arrivee:
            path_saved.append(path)
        
        # --- Sinon crée 4 chemins à partir des voisins de la dernière position
        # du chemin précédent
        else:
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
                if (x2,y2) not in seen_positions and 0 <= x2 < nl and 0 <= y2 < nc \
                and map_joueurs[x2,y2] != -1 and map_joueurs[x2,y2] != 2:
                    path_list.append(path + [(x2, y2)])
                    seen_positions.add((x2, y2))
                    
def reformat(path,output):
    
    """
    Change le format des données en sortie des fonctions de path finding.
    
    Paramètres
    ----------
    
    output : str
        Format des données en sortie. 'path' pour le chemin brut, 'direction'
        pour la prochaine direction à prendre, 'length' pour la longueur du
        chemin, 'directions' pour la liste des directions et 'arrivee' pour
        la position du point d'arrivee.
        
    """
    
    if output == 'path':
        return path
    elif output == 'length':
        return len(path)
    elif output == 'direction':
        if len(path) > 1:
            l1,c1 = path[0]
            l2,c2 = path[1]
            direction = l2-l1,c2-c1
        else:
            direction = (0,0)
        return direction
    elif output == 'directions':
        n = len(path)
        directions = [0]*(n-1)
        for k in range(n-1):
            l1,c1 = path[k]
            l2,c2 = path[k+1]
            directions[k] = l2-l1,c2-c1
        return directions      
    elif output == 'arrivee':
        return [path[-1]]
    return
