## Fichier Ligne.py
## ??

import numpy as np
from Vect2D import *
import Variables as Var

class ligne:
    def __init__(self, pos1 = vect2D(), pos2 = vect2D(), canvas = "", color = "black") :
        self.pos1 = pos1        # ??
        self.pos2 = pos2        # ??
        self.canvas = canvas    # ?? 
        self.color = color      # ??
        self.id = canvas.create_line(pos1.x,pos1.y,pos2.x,pos2.y, fill=color, arrow="last") # ??
        
    def raffraichir(self) :
        self.canvas.coords(self.id, self.pos1.x, self.pos1.y, self.pos2.x, self.pos2.y)
        return
        
def init_ligne(terrain):
    '''Permet d'afficher les vecteurs'''
    Var.Tligne=np.array([[ligne(canvas = terrain)] * Var.largeur] * Var.hauteur, ligne)
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.Tligne[y,x] = ligne(canvas = terrain)
    return
    
def cacher_ligne() :
    '''Permet de cacher les vecteurs'''
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.Tligne[y,x].pos1 = vect2D()
            Var.Tligne[y,x].pos2 = vect2D()
            Var.Tligne[y,x].raffraichir()
    return
