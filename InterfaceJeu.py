#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 21:43:20 2019

@author: alexis
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Tools import *
import ControleurJeu
import sys


class InterfaceJeu(QMainWindow):
    
    """
    La fenêtre de l'interface graphique du jeu.
    
    Attributs
    ----------
    
    menu : QWidget
        Le menu du jeu. Contient différents boutons pour lancer une partie,
        configurer les paramètres, etc.
        
    """
    
    def __init__(self):
        
        super().__init__()
        self.setWindowTitle('Menu du jeu MAMBA')        
        self.menu = MenuJeu(self)
        self.resize(400,500)
        self.setCentralWidget(self.menu)

       
class MenuJeu(QWidget):
    
    """
    Classe représentant le menu du jeu.
    
    Attributs
    ----------
    
    jouer : QPushButton
        Bouton permettant de lancer une nouvelle partie.
    options : QPushButton
        Bouton permettant d'afficher les options du jeu.
    quitter : QPushButton
        Bouton permettant de quitter le menu du jeu.
    params : QWidget
        Une instance de la classe OptionsJeu qui gère le menu des options.
        
    """
    
    def __init__(self, parent):
        
        super().__init__(parent)
        self.parent = parent
        
        # --- Création des boutons du menu
        self.jouer = QPushButton('Jouer')
        self.options = QPushButton('Options')
        self.params = OptionsJeu(self)
        self.quitter = QPushButton('Quitter')
        self.jouer.clicked.connect(self.lance_jeu)
        self.options.clicked.connect(self.affiche_options)
        self.quitter.clicked.connect(parent.close)
        
        # --- Disposition des boutons
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.jouer)
        layoutV.addWidget(self.options)
        layoutV.addWidget(self.params)
        layoutV.addWidget(self.quitter)        
        self.setLayout(layoutV)
        self.params.hide()
        
    def lance_jeu(self):
        
        """
        Méthode associée au bouton self.jouer. Lance une nouvelle partie.
        Ne fonctionne pas actuellement.
        
        """
#        params = self.params.get_params()
#        jeu = ControleurJeu.ControleurJeu(params,parent=None)
        
    def affiche_options(self):
        
        """
        Méthode associée au bouton self.options. Permet de dérouler le menu des
        options.
        
        """
        
        if self.params.isVisible():
            self.params.hide()
        else:
            self.params.show()

            
class OptionsJeu(QWidget):
    
    """
    Classe représentant le menu des options.
    
    Attributs
    ---------
    
    rb1_taille,rb2_taille,rb3_taille : QRadioButton
        Boutons permettant de sélectionner la taille des cases du terrain de
        jeu.
    
    rb1_cs,rb2_cs,rb3_cs : QRadioButton
        Boutons permettant de définir le contrôle du Serpent (Humain,
        IA aléatoire ou intermédiaire).

    rb1_cm,rb2_cm,rb3_cm,rb4_cm : QRadioButton
        Boutons permettant de définir le contrôle du Monstre (Humain,
        IA aléatoire, intermédiaire ou avancée).
    
    e1,e2 : QLineEdit
        Entrées texte permettant de définir la vitesse du Serpent / Monstre.
        
    """
    
    def __init__(self, parent):
        
        super().__init__(parent)
        grid = QGridLayout()
        
        box1 = QGroupBox(self)
        box1.setTitle('Taille des cases:')
        box1.setAlignment(Qt.AlignCenter)
        rbg_taille = QButtonGroup(self)
        self.rb1_taille = QRadioButton('Petite')
        self.rb2_taille = QRadioButton('Moyenne')
        self.rb2_taille.setChecked(True)
        self.rb3_taille = QRadioButton('Grande')
        rbg_taille.addButton(self.rb1_taille)
        rbg_taille.addButton(self.rb2_taille)
        rbg_taille.addButton(self.rb3_taille)
        layoutH1 = QHBoxLayout()
        layoutH1.addWidget(self.rb1_taille)
        layoutH1.addWidget(self.rb2_taille)
        layoutH1.addWidget(self.rb3_taille)
        box1.setLayout(layoutH1)
        
        box2 = QGroupBox(self)
        box2.setTitle('Contrôle du serpent:')
        box2.setAlignment(Qt.AlignCenter)
        rbg_cs = QButtonGroup(self)
        self.rb1_cs = QRadioButton('Humain')
        self.rb1_cs.setChecked(True)
        self.rb2_cs = QRadioButton('IA basique')
        self.rb3_cs = QRadioButton('IA avancée')
        rbg_cs.addButton(self.rb1_cs)
        rbg_cs.addButton(self.rb2_cs)
        rbg_cs.addButton(self.rb3_cs)
        layoutH2 = QHBoxLayout()
        layoutH2.addWidget(self.rb1_cs)
        layoutH2.addWidget(self.rb2_cs)
        layoutH2.addWidget(self.rb3_cs)
        box2.setLayout(layoutH2)
        
        box3 = QGroupBox()
        box3.setTitle('Contrôle du monstre:')
        box3.setAlignment(Qt.AlignCenter)
        rbg_cm = QButtonGroup(self)
        self.rb1_cm = QRadioButton('Humain')
        self.rb2_cm = QRadioButton('IA aléatoire')
        self.rb2_cm.setChecked(True)
        self.rb3_cm = QRadioButton('IA intermédiaire')
        self.rb4_cm = QRadioButton('IA avancée')
        layoutH3 = QHBoxLayout()
        rbg_cm.addButton(self.rb1_cm)
        rbg_cm.addButton(self.rb2_cm)
        rbg_cm.addButton(self.rb3_cm)
        rbg_cm.addButton(self.rb4_cm)
        layoutH3.addWidget(self.rb1_cm)
        layoutH3.addWidget(self.rb2_cm)
        layoutH3.addWidget(self.rb3_cm)
        layoutH3.addWidget(self.rb4_cm)
        box3.setLayout(layoutH3)
        
        
        box4 = QGroupBox()
        box4.setTitle('Vitesses des personnages (%)')
        box4.setAlignment(Qt.AlignCenter)
        self.e1 = QLineEdit()
        self.e2 = QLineEdit()
        self.e1.setText('1')
        self.e2.setText('1')
        flo = QFormLayout()
        flo.addRow('Serpent:', self.e1)
        flo.addRow('Monstre:', self.e2)
        box4.setLayout(flo)
        
        grid.setVerticalSpacing(30)
        grid.addWidget(box1)
        grid.addWidget(box2)
        grid.addWidget(box3)
        grid.addWidget(box4)
        self.setLayout(grid)

    def get_px_size(self):
        
        """ Renvoie la taille des cases du terrain. """
        
        px_size = 0
        if self.rb1_taille.isChecked():
            px_size = 8
        elif self.rb2_taille.isChecked():
            px_size = 10
        elif self.rb3_taille.isChecked():
            px_size = 15            
        return px_size

    def get_vitesses(self):
        
        """ Renvoie la vitesse du Serpent et du Monstre. """
        
        return float(self.e1.text()),float(self.e2.text())
    
    def get_params(self):
        
        """
        Renvoie un dictionnaire contenant l'ensemble des paramètres du jeu tels
        qu'ils sont définis dans le menu des options.
        
        """
        
        params = params_jeu()
        params["taille_case"] = self.get_px_size()
        params["vitesse_serpent"],params["vitesse_monstre"] = self.get_vitesses()
        
        if self.rb1_cs.isChecked():
            IA_serpent = 'Humain'
        elif self.rb2_cs.isChecked():
            IA_serpent = 'Aléatoire'
        elif self.rb3_cs.isChecked():
            IA_serpent = 'Intermédiaire'
        
        params["IA_serpent"] = IA_serpent
        
        if self.rb1_cm.isChecked():
            IA_monstre = 'Humain'
        elif self.rb2_cm.isChecked():
            IA_monstre = 'Aléatoire'
        elif self.rb3_cm.isChecked():
            IA_monstre = 'Intermédiaire'
        elif self.rb4_cm.isChecked():
            IA_monstre = 'Avancée'
        
        params["IA_monstre"] = IA_monstre
            
        return params
            
            
class FenetreJeu(QMainWindow):
    
    """
    Classe QMainWindow représentant la fenêtre du jeu.
    
    Attributs
    ---------
    
    key_serpent = Qt.Key
        Touche (Z,Q,S,D) pressée pour changer la direction du Serpent.
    key_monstre = Qt.Key
        Touche (I,J,K,L,H) pressée pour changer la direction du Monstre.
    key_annexe = Qt.Key
        Touche (P,Esc) pressée pour mettre le jeu en pause ou le fermer.
    carte : QGraphicsView
        Classe contenant le dessin du terrain.
        
    """
        
    def __init__(self,params,jeu):
        
        super().__init__()
        self.setWindowTitle("Mamba")
        
        map_zones = jeu.terrain.zones
        map_joueurs = jeu.terrain.joueurs
        taille_case = params["taille_case"]
        vs,vm = params["vitesse_serpent"],params["vitesse_monstre"]
        nl,nc = params["taille_terrain"]        
        self.key_serpent = None
        self.key_monstre = None
        self.key_annexe = None
        self.carte = CarteJeu(self,map_zones,map_joueurs,taille_case)
        self.setCentralWidget(self.carte)
    
    def keyPressEvent(self, event):
        
        """ Change les attributs key en appuyant sur une touche du clavier. """
        
        if event.isAutoRepeat():
            event.ignore()
        else:
            self.key = key = event.key()
            if key == Qt.Key_Escape or key == Qt.Key_P:
                self.key_annexe = key
            
            elif key in [Qt.Key_Z,Qt.Key_Q,Qt.Key_S,Qt.Key_D]:
                self.key_serpent = key
        
            elif key in [Qt.Key_I,Qt.Key_J,Qt.Key_K,Qt.Key_L,Qt.Key_H]:
                self.key_monstre = key
        return
           
                
class CarteJeu(QGraphicsView):
    
    """ QGraphicsView contenant le dessin du terrain de jeu.
    
    Paramètres
    ----------
    
    parent : QMainWindow
        La fenêtre "mère" de la classe.
    map_zones, map_joueurs : np.ndarray
        La matrice des zones / joueurs du terrain.
    taille_case : int
        La taille (en px) d'une case du terrain de jeu.
    
    Attributs
    ---------
    
    dessin : QGraphicsScene
        Le dessin du terrain de jeu.
    
    """
    
    def __init__(self,parent,map_zones,map_joueurs,taille_case):
        
        super().__init__(parent)
        self.dessin = DessinCarte(self,map_zones,map_joueurs,taille_case)
        self.setScene(self.dessin)
        

class DessinCarte(QGraphicsScene):
    
    """ QGraphicsScene correspondant au dessin du terrain de jeu.
    
    Paramètres
    ----------
    
    parent : QMainWindow
        La fenêtre "mère" du dessin.
    map_zones, map_joueurs : np.ndarray
        La matrice des zones / joueurs du terrain.
    taille_case : int
        La taille (en px) d'une case du terrain de jeu.
        
    """
    
    def __init__(self,parent,map_zones,map_joueurs,taille_case):
        
        super().__init__(parent)
        self.parent = parent
        px = taille_case
        nl,nc = map_zones.shape
        self.setSceneRect(0,0,nc*px,nl*px)
        
        self.brosse_grise = QBrush(QColor(128,128,128),Qt.SolidPattern)
        self.brosse_blanche = QBrush(QColor(255,255,255),Qt.SolidPattern)
        self.brosse_marron = QBrush(QColor(88,41,0),Qt.SolidPattern)
        self.brosse_rouge = QBrush(QColor(255,0,0),Qt.SolidPattern)
        self.brosse_bleue = QBrush(QColor(0,0,255),Qt.SolidPattern)
        self.stylo = QPen(Qt.black,1,Qt.SolidLine)
        self.px = px
        
        for i in range(nl):
            for k in range(nc):
                
                zone_danger,type_joueur = map_zones[i,k],map_joueurs[i,k]
                
                if zone_danger: # Zone non-safe
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_blanche)
                else: # Zone safe
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_grise)
                
                if type_joueur == 1: # Tete du serpent
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_rouge)
                elif type_joueur == -1: # Corps du serpent
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_marron)
                elif type_joueur == 2: # Monstre
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_bleue)    
        return
    
    def redessine(self,terrain,personnage,type_personnage):
        
        """
        Redessine le serpent ou le monstre lors d'un déplacement.
        
        Paramètres
        ----------
        
        terrain : Terrain
        personnage : Serpent ou Monstre
        type_personnage : str
            'Serpent' ou 'Monstre' selon qui l'on souhaite redessiner.
        
        """
        map_zones = terrain.zones
        nl,nc = terrain.size
        l1,c1 = personnage.position
        dl,dc = personnage.direction
        l0,c0 = (l1-dl)%nl,(c1-dc)%nc
        px = self.px
        
        
        if type_personnage == 'Serpent':
            
            if map_zones[l0,c0] == 1:
                self.addRect(c0*px,l0*px,px,px,self.stylo,self.brosse_marron)
                
            else:
                self.addRect(c0*px,l0*px,px,px,self.stylo,self.brosse_grise)
            
            self.addRect(c1*px,l1*px,px,px,self.stylo,self.brosse_rouge)    
            
        elif type_personnage == 'Monstre':
            
            self.addRect(c0*px,l0*px,px,px,self.stylo,self.brosse_blanche)
            self.addRect(c1*px,l1*px,px,px,self.stylo,self.brosse_bleue)            
        
        self.parent.setScene(self)
        
        
    def grise_dessin(self,corps,rr,cc):
        
        """
        Grise la zone délimitée par le serpent.
        
        Paramètres
        ----------
        
        corps : list
            La liste des coordonées des cases appartenant au corps du serpent.
        rr : numpy.ndarray
            Vecteur contenant l'indice (en ligne) des points à griser.
        cc : numpy.ndarray
            Vecteur contenant l'indice (en colonne) des points à griser.
        
        """
        
        px = self.px
        
        for case in corps:
            l,c = case
            self.addRect(c*px,l*px,px,px,self.stylo,self.brosse_grise)
        for k in range(len(rr)):
            l,c = rr[k],cc[k]
            self.addRect(c*px,l*px,px,px,self.stylo,self.brosse_grise)
        
        self.parent.setScene(self)
