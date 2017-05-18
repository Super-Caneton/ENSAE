from math import*

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
        
        
        
def p_scal(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.x + vecteur1.y * vecteur2.y
    
def projection(vecteur1, vecteur2): #projection du vecteur "vecteur1" sur le vecteur "vecteur2"
    return p_scal(vecteur1, vecteur2.normalise())*vecteur2.normalise()
