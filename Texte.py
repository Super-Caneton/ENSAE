from Vect2D import*
import numpy as np
import Variables as Var

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
        
        
##Affichage des distances
def init_texte(terrain):
    global Ttexte
    Var.Ttexte=np.array([[texte(canvas=terrain)]*Var.largeur]*Var.hauteur,texte)
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.Ttexte[y,x]=texte(vect2D(x,y)*Var.dimCase+vect2D(1,1)*(Var.dimCase/2), canvas=terrain)
    return
    
def cacher_texte() :
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.Ttexte[y,x].mot = ""
            Var.Ttexte[y,x].raffraichir()
    return
