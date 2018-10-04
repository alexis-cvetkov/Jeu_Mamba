# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



# =============================================================================
#                       Importation de modules
# =============================================================================



import numpy as np
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IPython.display import clear_output



# =============================================================================
#                               Classe Jeu
# =============================================================================



class Jeu(QMainWindow):
    
    def __init__(self,nl,nc,marge,px):
        
        """
        Crée un objet de la classe Jeu.
        
        Attributs
        ---------
        
        map_zones : cf init_map
        map_joueurs : cf init_map
        serpent : cf class Serpent
        px : taille d'une case du jeu en pixels.
        """
        self.map_zones = init_map(nl,nc,marge,type = 'zones')
        self.map_joueurs = init_map(nl,nc,marge,type = 'joueurs')
        self.v_NaN = np.empty((nl,1))
        self.v_NaN[:] = np.nan
        self.serpent = Personnage(position_initiale=(0,0),direction_initiale='droite',type_personnage='Serpent')
        #self.monstre = Monstre()
        
        self.px = px
        self.pause = False
        super().__init__()
        self.setWindowTitle("Mamba")
        self.environnement = Environnement(self,self.map_zones,self.map_joueurs,self.px)
        self.setCentralWidget(self.environnement)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10000//px)
        
    def keyPressEvent(self, event):
        
        """ Déplace le serpent lorsqu'on appuie sur une flèche directionnelle. """
        
        if event.isAutoRepeat():
            event.ignore()
           
        key = event.key()
        old_direction = self.serpent.old_direction
            
        if key == Qt.Key_Z:
            new_direction = 'haut' #variabe contenant la nouvelle direction 
        elif key == Qt.Key_D:
            new_direction = 'droite'
        elif key == Qt.Key_S:
            new_direction = 'bas'
        elif key == Qt.Key_Q:
            new_direction = 'gauche'
        elif key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_P: # On passe le jeu en pause / continue
            self.pause = not self.pause
            new_direction = old_direction # le serpent continue dans la meme direction après la pause.
        else:
            event.ignore()
        
        if not self.pause:
            
            commandes_invalides = [('gauche','droite'),('droite','gauche'),('bas','haut'),('haut','bas')]
            if not (old_direction,new_direction) in commandes_invalides:
                self.serpent.change_direction(new_direction)
                
        event.accept()
        
    def update(self):
        
        if not self.pause:
            
            self.serpent.deplace(self.map_joueurs,self.map_zones,self.environnement)
            qApp.processEvents() # Nécéssaire pour éviter le clignotement entre deux frames.
            self.setCentralWidget(self.environnement)
            
            if self.serpent.etat == 2: # On rentre à nouveau dans la zone safe donc on grise la zone dessinée.
                self.grise_zone()
                self.serpent.etat = 0
        
    def grise_zone(self):
        
        path = path_finding(self.map_zones,self.serpent.depart,self.serpent.arrivee)
                            
        for case in self.serpent.corps:
            self.map_zones[case] = 0
        
        #polygon = Polygon(self.serpent.corps)        
        self.environnement.carte.grise_dessin(self.serpent.corps+path,self.environnement)
        qApp.processEvents() # Nécéssaire pour éviter le clignotement entre deux frames.
        self.setCentralWidget(self.environnement)
        
        self.serpent.corps = []
        


# =============================================================================
#                            Classe Personnage
# =============================================================================



class Personnage():
    
    def __init__(self,position_initiale,direction_initiale,type_personnage):
            
        """
        Crée le monstre.
        
        Attributs
        ---------
        
        position : tuple donnant la position du serpent dans la matrice.
        direction : string donnant la direction.
        corps : liste des positions des cases mangées.
        
        """
        
        self.position = position_initiale
        self.direction_instant = direction_initiale #la direction à un instant t
        self.corps = []
        self.type = type_personnage
        self.old_direction = '' # direction lors de la dernière update de la map 
        self.etat = 0
        self.depart = (0,0)
        self.arrivee = (0,0)
        
    def change_direction(self,direction):
        
        self.direction_instant = direction
    
    def deplace(self,map_joueurs,map_zones,environnement):
        
        """ Modifie les matrices map_zones et map_joueurs lors du déplacement du serpent. """
        
        if self.type == 'Serpent':
            
            direction = self.direction_instant
            x,y = self.position
            old_position = x,y
            nl,nc = map_joueurs.shape
        
            if direction == 'droite':
                self.position = x,(y+1)%(nc)
                
            if direction == 'bas':
                self.position = (x+1)%(nl),y
                
            if direction == 'gauche':
                self.position = x,(y-1)%(nc)
                
            if direction == 'haut':
                self.position = (x-1)%(nl),y
            
            self.test_collisions() # Verifie que le serpent ne meurt pas pendant son déplacement.
            new_position = self.position        
            old_zone,new_zone = map_zones[old_position],map_zones[new_position]
            
            if  old_zone != new_zone : # Changement de zone.
                self.etat += 1
                if self.etat == 1:
                    self.depart = old_position
                else:
                    self.arrivee = new_position
            
            if old_zone:
                map_joueurs[old_position] = -1
            
            else:
                map_joueurs[old_position] = 0
            
            map_joueurs[new_position] = 1
            
            if new_zone:
                self.corps.append(new_position)
            
            environnement.carte.redessine(old_position,new_position,old_zone,new_zone,environnement)
            
            self.old_direction = self.direction_instant
        
    def test_collisions(self):
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
        self.brosse_verte = QBrush(QColor(0,255,0),Qt.SolidPattern)
        self.stylo = QPen(Qt.black,1,Qt.SolidLine)
        self.px = px
        
        for i in range(nl):
            for k in range(nc):
                if map_zones[i,k]:
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_blanche)
                else:
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_grise)
                if map_joueurs[i,k] == 1:
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_rouge)
                elif map_joueurs[i,k] == -1:
                    self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_marron)
    
     
    def redessine(self,old_position,new_position,old_zone,new_zone,environnement):
        
        i,k = old_position
        px = self.px
        
        if old_zone:
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_marron)
            
        else:
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_grise)
        
        i,k = new_position
        self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_rouge)    
        
        environnement.setScene(self)
        
    def grise_dessin(self,zone_a_griser,environnement):
        
        px = self.px
        
        for case in zone_a_griser:
            i,k = case
            self.addRect(k*px,i*px,px,px,self.stylo,self.brosse_verte)
        
        environnement.setScene(self)    
            


# =============================================================================
#                           Fonctions secondaires
# =============================================================================



def fill_contours(array):
    return np.maximum.accumulate(array,1) & \
           np.maximum.accumulate(array[:,::-1],1)[:,::-1]


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


# =============================================================================
#                               Fonction Main
# =============================================================================



def main(nl,nc,marge,px):
    
    """ Lance le jeu et affiche l'interface graphique."""
    
    app = QApplication(sys.argv)
    jeu = Jeu(nl,nc,marge,px)
    M = jeu.map_zones
    jeu.show()
    #jeu.resize(1600,900)
    app.exec_()
    #sys.exit(app.exec_())
    return M

    
M = main(20,40,2,20)