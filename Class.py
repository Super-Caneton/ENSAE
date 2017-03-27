from math import *
from random import *

class vect2D:    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
## Addition de vecteurs
    def __iadd__(self, vecteur):
        if type(vecteur) == vect2D:
            self.x += vecteur.x
            self.y += vecteur.y
            return self
    def __add__(vecteur1, vecteur2):
        if type(vecteur1) == vect2D and type(vecteur2) == vect2D:
            nVecteur = vect2D()
            nVecteur += vecteur1
            nVecteur += vecteur2
            return nVecteur
    def __isub__(self, vecteur):
        if type(vecteur) == vect2D:
            self.x -= vecteur.x
            self.y -= vecteur.y
            return self
    def __sub__(vecteur1, vecteur2):
        if type(vecteur1) == vect2D and type(vecteur2) == vect2D:
            nVecteur = vect2D()
            nVecteur += vecteur1
            nVecteur -= vecteur2
            return nVecteur
        
## Multiplication par un scalaire
    def __imul__(self, scalaire):
        if type(scalaire) == int or type(scalaire) == float:
            self.x *= scalaire
            self.y *= scalaire
            return self
    def __mul__(vecteur, scalaire):
        if (type(scalaire) == int or type(scalaire) == float) and type(vecteur) == vect2D:
            nVecteur = vecteur
            nVecteur *= scalaire
            return nVecteur
    def __rmul__(vecteur, scalaire):
        if (type(scalaire) == int or type(scalaire) == float) and type(vecteur) == vect2D:
            return vecteur * scalaire

## Affichage d'un vecteur
    def __str__(self):
        return "[{},{}]".format(self.x,self.y)
    def __repr__(self):
        return "[{},{}]".format(self.x,self.y)
    
    
class randvect2D(vect2D):
    def __init__(self, xmin, xmax, ymin, ymax) :
        self.x = randint(xmin, xmax)
        self.y = randint(ymin, ymax)
    

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

            
        
        
