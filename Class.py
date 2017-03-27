from math import *
from random import *

class vect2D:    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
## Addition de vecteurs
    def __iadd__(self, vecteur):
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x += vecteur.x
        nVecteur.y += vecteur.y
        return nVecteur
    def __add__(self, vecteur):
        nVecteur = self
        nVecteur += vecteur
        return nVecteur
    def __isub__(self, vecteur):
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x -= vecteur.x
        nVecteur.y -= vecteur.y
        return nVecteur
        return nVecteur
    def __sub__(self, vecteur):
        nVecteur = self
        nVecteur -= vecteur
        return nVecteur
        
## Multiplication par un scalaire
    def __imul__(self, scalaire):
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur.x += scalaire
        nVecteur.y += scalaire
        return nVecteur
    def __mul__(self, scalaire):
        nVecteur = vect2D()
        nVecteur.x = self.x
        nVecteur.y = self.y
        nVecteur *= scalaire
        return nVecteur
    def __rmul__(self, scalaire):
        return self * scalaire

## Affichage d'un vecteur
    def __str__(self):
        return "[{},{}]".format(self.x,self.y)
    def __repr__(self):
        return "[{},{}]".format(self.x,self.y)

##Méthodes
    def norme(self) :
        return sqrt(self.x**2+self.y**2)
    
    
class randvect2D(vect2D):
    def __init__(self, xmin, xmax, ymin, ymax) :
        self.x = uniform(xmin, xmax)
        self.y = uniform(ymin, ymax)
    

class individu:
    def __init__(self, pos, dpos, r, m, canvas, color):
        self.pos = pos
        self.dpos = dpos
        self.r = r
        self.m = m
        self.canvas = canvas
        self.id = canvas.create_oval(-1*r, -1*r, r, r, fill=color)
        self.canvas.move(self.id, pos.x, pos.y)


class mur:
    def __init__(self, pos, dimension, angle, canvas, color):
        self.pos = pos
        self.dimension = dimension
        self.angle = angle #l'angle est mesuré dans le sens horaire
        self.canvas = canvas

            
        
        
