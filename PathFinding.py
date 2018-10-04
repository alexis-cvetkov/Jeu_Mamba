#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:03:32 2018

@author: raphael
"""

import numpy as np
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IPython.display import clear_output

def init_map(nl,nc,marge,type):
    """
    Fonction qui initialise les matrices correspondant au plateau de jeu.
    
    Paramètres
    ----------
    
    nl : int
        Nombre le lignes du plateau de jeu.
    nc : int
        Nombre de colonnes du plateau de jeu.
    marge : int
        La marge définissant la zone safe.
    type : str
        Le type de matrice a créer. type = 'zones' (resp. 'joueurs') pour initialiser la matrice des zones
        (resp. des joueurs).
    
    Renvoie
    -------
    
    M : int array
        Si type = 'zones', M[i,k] = 0 si la case (i,k) est dans la zone safe et M[i,k] = 1 si elle est dans la zone
        de danger. Initiallement, une bordure de taille "marge" est créee pour la zone safe. Le reste de la carte
        correspond à la zone de danger.
        Si type = 'joueurs', M[i,k] = 1 la où le joueur se situe, -1 sur les cases non-safe mangées par le joueurs et
        0 pour le reste des cases.
        
    """
    
    if type == 'zones':
        
        M = np.zeros((nl,nc),dtype=int)
        M[marge:nl-marge,marge:nc-marge] = 1    
        
    elif type == 'joueurs':
        M = np.zeros((nl,nc),dtype=int)
        M[0,0] = 1
        
    else:
        print('Erreur')
        
    return M

def bfs(grid, start,goal):
    queue = [[start]]
    seen = set([start])
    nl,nc = grid.shape
    while queue:
        path = queue.pop(0)
        x, y = path[-1]
        if (x,y) == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < nl and 0 <= y2 < nc and grid[y2][x2] != 1 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


Map_zone = init_map(20,20,2,'zones')

path = bfs(Map_zone,(1,2),(16,18))

for x,y in path :
    Map_zone[x][y] = 2

Map_zone


