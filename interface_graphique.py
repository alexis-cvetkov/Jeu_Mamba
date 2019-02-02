#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 14:35:49 2019

@author: alexis
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class InterfaceJeu(QMainWindow):
    
    def __init__(self,screen_width,screen_height):
        
        super().__init__()
        self.setWindowTitle('Menu du jeu MAMBA')        
        self.menu = MenuJeu(self)
        self.setCentralWidget(self.menu)
        self.screen_width = screen_width
        self.screen_height = screen_height
        
class MenuJeu(QWidget):
    
    def __init__(self, parent):
        
        super().__init__(parent)
        
        self.parent = parent        
        self.jouer = QPushButton('Jouer')
        self.options = QPushButton('Options')
        self.params = OptionsJeu(self)
        self.quitter = QPushButton('Quitter')        
        
        self.jouer.clicked.connect(self.lance_jeu)
        self.options.clicked.connect(self.affiche_options)
        self.quitter.clicked.connect(parent.close)
        
        layoutV = QVBoxLayout(self)
        layoutV.addWidget(self.jouer)
        layoutV.addWidget(self.options)
        layoutV.addWidget(self.params)
        layoutV.addWidget(self.quitter)
        
        self.setLayout(layoutV)
        self.params.hide()
        
    def lance_jeu(self):
        
        px_size = self.params.get_px_size()
        vitesses = self.params.get_vitesses()
        w,h = self.parent.screen_width,self.parent.screen_height
        self.parent.jeu = Jeu(w,h,px_size,vitesses,self.parent)
        self.parent.jeu.showFullScreen()
        
    def affiche_options(self):
        
        if self.params.isVisible():
            self.params.hide()
        else:
            self.params.show()
    
class OptionsJeu(QWidget):
    
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
        self.rb2_cm = QRadioButton('IA basique')
        self.rb2_cm.setChecked(True)
        self.rb3_cm = QRadioButton('IA avancée')
        layoutH3 = QHBoxLayout()
        rbg_cm.addButton(self.rb1_cm)
        rbg_cm.addButton(self.rb2_cm)
        rbg_cm.addButton(self.rb3_cm)
        layoutH3.addWidget(self.rb1_cm)
        layoutH3.addWidget(self.rb2_cm)
        layoutH3.addWidget(self.rb3_cm)
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
        
        px_size = 0
        if self.rb1_taille.isChecked():
            px_size = 8
        elif self.rb2_taille.isChecked():
            px_size = 10
        elif self.rb3_taille.isChecked():
            px_size = 15            
        return px_size

    def get_vitesses(self):
        
        return float(self.e1.text()),float(self.e2.text())


# =============================================================================
#                       Importation de modules
# =============================================================================

import numpy as np
import sys
from random import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from IPython.display import clear_output
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

import time

# =============================================================================
#                               Classe Jeu
# =============================================================================

class Jeu(QMainWindow):
    
    def __init__(self,width,height,px,vitesses,parent = None):
        
        """
        Crée un objet de la classe Jeu.
        
        Attributs
        ---------
        
        map_zones : cf init_map
        map_joueurs : cf init_map
        serpent : cf class Serpent
        px : taille d'une case du jeu en pixels.
        
        """
        
        nl,nc = int(0.8*height/px),int(0.8*width/px)
        marge = nc//10
        pos_serpent,pos_monstre = (0,0),(nl//2,nc//2)
        self.serpent = Personnage(pos_serpent,direction_initiale=(0,1),type_personnage='Serpent')
        self.monstre = Personnage(pos_monstre,direction_initiale=(0,-1),type_personnage='Monstre') # On place le monstre au centre de la carte.
        self.map_zones = init_map(nl,nc,marge,pos_serpent,pos_monstre,type = 'zones')
        self.map_joueurs = init_map(nl,nc,marge,pos_serpent,pos_monstre,type = 'joueurs')
        
        self.px = px
        self.pause = False
        super().__init__(parent)
        self.setWindowTitle("Mamba")
        self.environnement = Environnement(self,self.map_zones,self.map_joueurs,self.px)
        self.setCentralWidget(self.environnement)
        
        vs,vm = vitesses
        self.timer_serpent = QTimer()
        self.timer_serpent.timeout.connect(self.update_serpent)
        self.timer_serpent.start(int(5000/(vs*nc)))
        self.timer_monstre = QTimer()
        self.timer_monstre.timeout.connect(self.update_monstre)
        self.timer_monstre.start(int(5000/(vm*nc)))
        
        self.periode_timer = int(5000/(vs*nc))
        self.periodes_update = []
        
    def keyPressEvent(self, event):
        
        """ Déplace le serpent lorsqu'on appuie sur une flèche directionnelle. """
        
        if event.isAutoRepeat():
            event.ignore()
           
        key = event.key()
        dl,dc = self.serpent.old_direction # Old direction
        
        if key == Qt.Key_Escape:
            self.close()
        
        elif key == Qt.Key_P: # On passe le jeu en pause / continue
            if self.pause:
                self.timer_serpent.start()
                self.timer_monstre.start()
            else:
                self.timer_serpent.stop()
                self.timer_monstre.stop()
            self.pause = 1 - self.pause
        
        else:
            if key == Qt.Key_Z:
                dl2,dc2 = (-1,0) # Variable contenant la nouvelle direction 
            elif key == Qt.Key_D:
                dl2,dc2 = (0,1)
            elif key == Qt.Key_S:
                dl2,dc2 = (1,0)
            elif key == Qt.Key_Q:
                dl2,dc2 = (0,-1)
            
            if not (self.pause or dl+dl2 == 0 or dc+dc2 == 0):
                self.serpent.change_direction((dl2,dc2))
            
            else:
                event.ignore()
                
        
    def update_serpent(self):
        

        mapZ,mapJ = self.map_zones,self.map_joueurs
        self.serpent.deplace(mapZ,mapJ,self.environnement)
        self.test_collision()
        if self.serpent.etat == 2: # On rentre à nouveau dans la zone safe donc on grise la zone dessinée.
            self.grise_zone()
            self.serpent.etat = 0
        #qApp.processEvents() # Nécéssaire pour éviter le clignotement entre deux frames.
        #self.setCentralWidget(self.environnement)
        
    def update_monstre(self):
        t1 = time.time()
        mapZ,mapJ = self.map_zones,self.map_joueurs
        self.monstre.genere_direction(mapZ,mapJ,self.serpent,'avancée')
        self.monstre.deplace(mapZ,mapJ,self.environnement)
        #qApp.processEvents() # Nécéssaire pour éviter le clignotement entre deux frames.
        #self.setCentralWidget(self.environnement)    
        self.periodes_update.append((time.time()-t1)*1000)
        
    def grise_zone(self):
        
        path = path_finding(self.map_zones,self.serpent.depart,self.serpent.arrivee)
        path.reverse()
        
        for case in self.serpent.corps:
            self.map_zones[case] = 0
        
        contour = self.serpent.corps + path # L'ordre des points est important pour delimiter le polygone correctement.
        polygon = Polygon(contour)
        
        L,C = zone_a_tester(contour)
        nl,nc = L.shape 
        points_a_griser = self.serpent.corps
        for i in range(nl):
            for k in range(nc):
                coordonnees = L[i,k],C[i,k]
                point = Point(coordonnees)
                if polygon.contains(point):
                    points_a_griser.append(coordonnees)
                    self.map_zones[coordonnees] = 0
                    pass
        
        self.environnement.carte.grise_dessin(points_a_griser,self.environnement)
        qApp.processEvents() # Nécéssaire pour éviter le clignotement entre deux frames.
        self.setCentralWidget(self.environnement)
        
        self.serpent.corps = []
        
    def test_collision(self):
        
        corps = self.serpent.corps.copy()
        #tete = [self.serpent.position]
        if corps != []:
            corps.pop()
        # Test si le serpent se mord la queue.
        if self.serpent.position in corps:
            self.timer_serpent.stop()
            self.timer_monstre.stop()
            self.pause = 1 - self.pause
        #test si le monstre mange le corps du serpent
        #elif self.monstre.position in serpent:
         #   self.close()
        return

# =============================================================================
#                            Classe Personnage
# =============================================================================



class Personnage():
    
    def __init__(self,position_initiale,direction_initiale,type_personnage):
            
        """
        Crée le personnage.
        
        Attributs
        ---------
        
        position : tuple donnant la position du personnage dans la matrice.
        direction : string donnant la direction.
        corps : liste des positions des cases mangées dans le cas du serpent.
        type : le type de personnage ('Monstre' ou 'Serpent').
        old_direction : la direction lors du dernier déplacement du personnage.
        depart : la dernière case safe ou est passé le serpent avant d'entrer en zone pas safe.
        arrivee : la première case safe ou rentre le serpent avant de quitter la zone pas safe.
        
        """
        
        self.position = position_initiale
        self.direction_instant = direction_initiale # la direction à un instant t
        self.corps = []
        self.type = type_personnage
        self.old_direction = '' # direction lors de la dernière update de la map 
        self.etat = 0
        self.depart = (0,0)
        self.arrivee = (0,0)
        
    def change_direction(self,direction):
        
        self.direction_instant = direction
    
    def deplace(self,map_zones,map_joueurs,environnement):
        
        """ Modifie les matrices map_zones et map_joueurs lors du déplacement du personnage. """
        
        if self.direction_instant == (0,0):
            return
        
        l,c = self.position
        dl,dc = self.direction_instant
        nl,nc = map_joueurs.shape
    
        # Calcul les nouvelles positions.
        
        old_position = l,c
        new_position = (l+dl)%nl,(c+dc)%nc
        self.test_collisions(new_position) # Verifie que le serpent ne meurt pas pendant son déplacement.
        
        self.position = new_position
        old_zone,new_zone = map_zones[old_position],map_zones[new_position]
        
        if  old_zone != new_zone : # Changement de zone.            
            self.etat += 1
            if self.etat == 1:
                self.depart = l,c
            else:
                self.arrivee = new_position
        
        if self.type == 'Serpent':
            
            if old_zone:
                map_joueurs[old_position] = -1            
            else:
                map_joueurs[old_position] = 0
            
            map_joueurs[new_position] = 1
            
            if new_zone:
                self.corps.append(new_position)
        
        elif self.type == 'Monstre':
            
            map_joueurs[old_position] = 0
            map_joueurs[new_position] = 2
        
        environnement.carte.redessine(old_position,new_position,old_zone,new_zone,
                                      environnement,self.type)
        
        self.old_direction = self.direction_instant
        
    def possible_directions(self,map_zones):
        l,c = self.position
        nl,nc = map_zones.shape
        D = [(1,0),(-1,0),(0,1),(0,-1)] # Bas, Haut, Droite, Gauche.
        dx,dy = self.direction_instant
        D.remove((-dx,-dy))
        directions = D.copy()
        for d in D:
            dl,dc = d
            p = (l+dl)%nl,(c+dc)%nc
            if not map_zones[p]:
                directions.remove(d)
        return directions
    
    def genere_direction(self,map_zones,map_joueurs,serpent,IA='aleatoire'):
        
        D = self.possible_directions(map_zones)#return the possible directions list
        
        if IA == 'aleatoire' :
            
            if random() > 0.95:#5% chances of changing the direction
                
                if D == []: # entity surrounded by gray cases.
                    self.change_direction((0,0)) # immobile monster
                else:
                     self.change_direction(choice(D))
            else:#case when the monster doesn't need to change direction
                if self.direction_instant not in D:#test if it can continue in the same direction
                    if D == []:
                        self.change_direction(choice(D))
                    else:
                        self.change_direction(choice(D))
                
            
        elif IA == 'intermédiaire' :#pathFindinf only if the serpent is in the unsafe zone 

        
            if map_zones[serpent.position] == 1:#serpent is in the unsafe zone => pathFinding behaviour
                
                self.change_direction(path_finding2(map_zones,self.position,serpent.corps))
                
             
            else: #Serpent is in the safe zone => random behaviour
                self.genere_direction(map_zones,map_joueurs,'aleatoire')
                #position_finale  = path_finding(map_zones, serpent.position,)
                
        elif IA == 'avancée':
            
            if map_zones[serpent.position] == 1:#serpent is in the unsafe zone => pathFinding behaviour
                
                self.change_direction(path_finding2(map_zones,self.position,serpent.corps))
                
            else:
                
                self.change_direction(path_finding2(map_zones,self.position,path_finding3(map_zones, serpent.position)))
                
            return           
    
#    def path_finding(grid,depart,arrivee):
#    
#    queue = [[depart]]
#    seen = set([depart])
#    nl,nc = grid.shape
#    
#    while queue:       
#        
#        path = queue.pop(0)
#        x, y = path[-1]
#        
#        if (x,y) == arrivee:
#            return path
#        
#        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
#            if 0 <= x2 < nl and 0 <= y2 < nc and grid[x2][y2] == 1 and (x2, y2) not in seen:
#                queue.append(path + [(x2, y2)])
#                seen.add((x2, y2))

    
    
    def test_collisions(self,new_position):
        pass
    
    
    
# =============================================================================
#                            Classe Environnement
# =============================================================================
        
    
    
class Environnement(QGraphicsView):
    
    """ Classe qui dessine la carte à partir de map_zones et map_joueurs. """
    
    def __init__(self,parent,map_zones,map_joueurs,px):
        
        super().__init__(parent)
        self.carte = Carte(self,map_zones,map_joueurs,px)
        self.setScene(self.carte)
        

class Carte(QGraphicsScene):
    
    def __init__(self,parent,map_zones,map_joueurs,px):
        
        super().__init__(parent)
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
    
    def redessine(self,old_position,new_position,old_zone,new_zone,environnement,
                  type_personnage):
        
        i,k = old_position
        px = self.px
        
        if type_personnage == 'Serpent':
            
            if old_zone:
                self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_marron)
                
            else:
                self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_grise)
            
            i,k = new_position
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_rouge)    
            
        else:
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_blanche)
            i,k = new_position
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_bleue)            
        
        environnement.setScene(self)
        
    def grise_dessin(self,zone_a_griser,environnement):
        
        px = self.px
        
        for case in zone_a_griser:
            i,k = case
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_grise)
        
        environnement.setScene(self)    
            


# =============================================================================
#                           Fonctions secondaires
# =============================================================================


def init_map(nl,nc,marge,pos_serpent,pos_monstre,type):
    
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
        M[pos_serpent] = 1
        M[pos_monstre] = 2
        
    return M


def path_finding(grid,depart,arrivee):
    
    queue = [[depart]]
    seen = set([depart])
    nl,nc = grid.shape
    
    while queue:       
        
        path = queue.pop(0)
        x, y = path[-1]
        
        if (x,y) == arrivee:
            return path
        
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
            if 0 <= x2 < nl and 0 <= y2 < nc and grid[x2][y2] != 1 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
                
def path_finding2(grid,depart,arrivee):
    
    queue = [[depart]]
    seen = set([depart])
    nl,nc = grid.shape
    
    while queue:       
        
        path = queue.pop(0)
        x, y = path[-1]
        
        if (x,y) in arrivee:
            x0, y0 = depart
            x1, y1 = path[1]
            return (x1-x0, y1-y0)
        
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
            if 0 <= x2 < nl and 0 <= y2 < nc and grid[x2][y2] == 1 and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def path_finding3(grid,depart):
    
    queue = [[depart]]
    seen = set([depart])
    nl,nc = grid.shape
    
    while queue:       
        
        path = queue.pop(0)
        x, y = path[-1]
        
        if grid[x,y] == 1:
            return [(x, y)]
        
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):            
            if 0 <= x2 < nl and 0 <= y2 < nc  and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def zone_a_tester(contour):
    
    lignes = [position[0] for position in contour]
    colonnes = [position[1] for position in contour]
    
    l_min,l_max = min(lignes),max(lignes)
    c_min,c_max = min(colonnes),max(colonnes)
    
    l = np.arange(l_min,l_max+1)
    c = np.arange(c_min,c_max+1)    
    L,C = np.meshgrid(l,c)
    
    return L,C
    
# =============================================================================
#                               Fonction Main
# =============================================================================

        
def main():
    
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()
    interface_jeu = InterfaceJeu(screen_width,screen_height)
    interface_jeu.show()
    interface_jeu.resize(324,496)
    app.exec()
    return interface_jeu.jeu

if __name__ == '__main__':
    jeu = main()
    print(jeu.periode_timer)
    print(sum(jeu.periodes_update)/len(jeu.periodes_update))