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
        nVecteur.x *= scalaire
        nVecteur.y *= scalaire
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
        
    def normalise(self) :
        if(self.norme() != 0) :
            return (1/self.norme())*self
        return self


class case:
    def __init__(self, pos=vect2D(), dim=0, type=0, score=0, canvas="", color="ivory", explore=False, grille=False) :
        self.pos = pos
        self.dim = dim
        self.type = type # -1 = infranchissable, 0=case normale, 1=sortie, (-2=danger, 2=escalier ?)
        self.score = score
        self.canvas = canvas
        self.color = color
        self.explore = explore
        self.grille = grille
        self.id = canvas.create_rectangle(0,0,dim,dim, fill=color, outline=color)
        self.canvas.move(self.id, pos.x*dim, pos.y*dim)
    
    def raffraichir(self) :
        if(self.type == -1) :
            self.color = "black"
        elif(self.type == 1) :
            self.color = "green"
        elif(self.type == -2) :
            self.color = "red"
        else :
            self.color = "ivory"
        if(self.grille):
            if(self.color == "black") :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "ivory")
            else :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "black")
        else :
            self.canvas.itemconfig(self.id, fill = self.color, outline = self.color)
        return
    
    #Change la couleur en faisant un dégradé entre fg et bg selon score et maxd
    def degrade(self, fg, bg, maxd):
        def blend(i,fg,bg) :
            return (int((1-i)*fg[0]+i*bg[0]), int((1-i)*fg[1]+i*bg[1]), int((1-i)*fg[2]+i*bg[2]))
        col = blend(self.score/maxd, fg, bg)
        if(self.grille) :
            if (col[0] > 255 or col[1] > 255 or col[2] > 255) :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "black")
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "black")
        else :
            if (col[0] > 255 or col[1] > 255 or col[2] > 255) :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "#%02x%02x%02x" % bg)
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "#%02x%02x%02x" % col)
        return
        

class ligne:
    def __init__(self, pos1=vect2D(), pos2=vect2D(), canvas="", color="black") :
        self.pos1 = pos1
        self.pos2 = pos2
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_line(pos1.x,pos1.y,pos2.x,pos2.y, fill=color, arrow="last")
        
    def raffraichir(self) :
        self.canvas.coords(self.id, self.pos1.x, self.pos1.y, self.pos2.x, self.pos2.y)
        return
        
class texte:
    def __init__(self, pos=vect2D(), mot="", canvas="", color="black") :
        self.pos = pos
        self.mot = mot
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_text(pos.x,pos.y, text=mot)
        
    def raffraichir(self) :
        self.canvas.coords(self.id, self.pos.x, self.pos.y)
        self.canvas.itemconfig(self.id, text=self.mot)
        return
    

class individu:
    def __init__(self, pos, dpos, r, canvas, color):
        self.pos = pos
        self.dpos = dpos
        self.r = r
        self.canvas = canvas
        self.color = color
        self.id = canvas.create_oval(-1*r, -1*r, r, r, fill=color, outline = color)
        self.canvas.move(self.id, pos.x, pos.y)
    
    def bouge(self) :
        self.canvas.move(self.id, self.dpos.x, self.dpos.y)
        self.pos += self.dpos
        return
        
            
        
        
