#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 12:25:38 2019

@author: alexis
"""

import numpy as np


class Terrain:
    
    """
    Crée une instance de la classe Terrain.
    
    Parametres
    ----------

    params : dict
        Un dictionnaire contenant les paramètres du jeu, notamment la
        taille du terrain.
        
    Attributs
    ---------
    
    zones : numpy.ndarray
        Une matrice représentant les différentes zones du terrain de jeu.
        Une case de cette matrice vaut 0 (respectivement 1) si elle
        appartient à la zone du Serpent (respectivement la zone du
        Monstre).
    joueurs : numpy.ndarray
        Une matrice indiquant la position des joueurs sur le terrain de
        jeu. Une case de cette matrice vaut 0 si elle est inoccupée, 1 ou
        -1 si la tête ou le corps du serpent s'y trouve et 2 si le monstre
        occupe la case.
    size : tuple
        La taille du terrain (nombre de lignes, nombre de colonnes).
    
    """
    
    def __init__(self,params):
        
        # --- Extraction dans params de la taille du terrain
        nl,nc = params["taille_terrain"]
        self.size = nl,nc
        
        # --- Création de la matrice associée aux zones
        marge = nc//10 # 10% du terrain
        map_zones = np.zeros(self.size,dtype=int)
        map_zones[marge:nl-marge,marge:nc-marge] = 1
        self.zones = map_zones
        
        # --- Création de la matrice associée aux joueurs
        map_joueurs = np.zeros(self.size,dtype=int)
        map_joueurs[0,0] = 1
        map_joueurs[nl//2,nc//2] = 2
        self.joueurs = map_joueurs
        
        return

class Monstre:
    
    """
    Classe représentant le Monstre du jeu.
    
    Paramètres
    ----------
    
    params : dict
            Un dictionnaire contenant les paramètres du jeu.
            
    Attributs
    ---------
    
    position : int tuple
        Indices (ligne,colonne) de la position du monstre dans la
        matrice représentant le terrain de jeu.
    direction : int tuple
        Valeurs (dligne,dcolonne) du déplacement élémentaire effectué
        par le monstre à chaque étape.
        Ex: (1,0) -> bas, (0,1) -> droite.
    IA : string
        Le type de joueur contrôlant le monstre. IA = 'Humain',
        'Aléatoire', 'Intermédiaire' ou 'Avancée'.
        
    """
        
    def __init__(self,params):
        
        nl,nc = params["taille_terrain"]
        self.position = nl//2,nc//2
        self.direction = (0,0)
        self.IA = params["IA_monstre"]
        return


class Serpent:

    """
    Classe représentant le Serpent du jeu.
    
    Paramètres
    ----------
    
    params : dict
            Un dictionnaire contenant les paramètres du jeu.
    
    Attributs
    ---------
    
    position : int tuple
        Indices (ligne,colonne) de la position du serpent dans la
        matrice représentant le terrain de jeu.
    direction : int tuple
        Valeurs (dligne,dcolonne) du déplacement élémentaire effectué
        par le serpent à chaque étape.
        Ex: (1,0) -> bas, (0,1) -> droite.
    IA : string
        Le type de joueur contrôlant le serpent. IA = 'Humain',
        'Aléatoire', 'Intermédiaire'.
    corps: list
        Une liste contenant les positions du "corps" du Serpent, càd les
        positions successives par lesquelles il est passé lors de sa trajet
        dans la zone du Monstre.
    cpt : int
        Un compteur incrémenté chaque fois que le Serpent change de zone.
        Initialisé à 0, il passe à 1 quand le Serpent rentre dans la zone
        du Monstre, puis atteint 2 lorsqu'il fini sa boucle et retourne
        dans sa zone. A ce moment, on grise la zone entourée et le compteur
        est remis à 0.
    depart : tuple
        La position du Serpent juste avant qu'il entre dans la zone du
        Monstre.
    arrivee : tuple
        La position du Serpent juste après être sorti de la zone du
        Monstre.
    
    """
    
    def __init__(self,params):
        
        self.position = 0,0
        self.direction = (0,1)
        self.IA = params["IA_serpent"]
        self.corps = []
        self.cpt = 0
        self.depart = (0,0)
        self.arrivee = (0,0)
        self.direction_list = []

        return