from Vect2D import*
import numpy as np
import random as rd
import Variables as Var

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
        
##
def touche_indiv(individu1, individu2) :
    return (individu1.pos - individu2.pos).norme() <= individu1.r+individu2.r


##
def init_indiv(terrain):
    supprime_indiv(terrain)
    for i in range(Var.NIndiv) :
        x = rd.uniform(Var.rIndiv, (Var.largeur-1)*Var.dimCase-Var.rIndiv)
        y = rd.uniform(Var.rIndiv, (Var.hauteur-1)*Var.dimCase-Var.rIndiv)
        while Var.TCase[int(y/Var.dimCase),int(x/Var.dimCase)].type < 0 :
            x = rd.uniform(Var.rIndiv, (Var.largeur-1)*Var.dimCase-Var.rIndiv)
            y = rd.uniform(Var.rIndiv, (Var.hauteur-1)*Var.dimCase-Var.rIndiv)
        pos = vect2D(x,y)
        dpos = vect2D(0,0)
        indiv=individu(pos, dpos, Var.rIndiv, terrain,"red")
        Var.LIndiv.append(indiv)
    return

def supprime_indiv(terrain) :
    for i in Var.LIndiv :
        terrain.delete(i.id)
    Var.LIndiv = []
    return
    
def sortir_indiv(terrain) :
    for individu in Var.LIndiv :
        x=int(individu.pos.x/Var.dimCase)
        y=int(individu.pos.y/Var.dimCase)
        if(Var.TCase[y,x].type==1) :
            terrain.delete(individu.id)
            Var.LIndiv.remove(individu)
    return
    
def bouge_indiv() :
    for i, individu1 in enumerate(Var.LIndiv) :
        x=int(individu1.pos.x/Var.dimCase)
        y=int(individu1.pos.y/Var.dimCase)
        individu1.dpos += Var.Tdirection[y,x]
        for individu2 in Var.LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1,individu2)
        rebond_bord(individu1)
        rebond_mur(individu1)
        individu1.dpos = individu1.dpos.normalise()*rd.uniform(Var.vminIndiv,Var.vmaxIndiv)
        individu1.bouge()
    return
    
    
##Gestion des rebonds
def rebond_indiv(individu1, individu2) : 

    n = individu1.pos - individu2.pos
    
    n1 = projection(individu1.dpos, n)
    n2 = projection(individu2.dpos, n)
    
    t1 = individu1.dpos - n1
    t2 = individu2.dpos - n2
    
    individu1.dpos = (t1 + n2)
    individu2.dpos = (t2 + n1)
    
    return
    
def rebond_mur(individu) :
    pos = individu.pos
    r = individu.r
    c = Var.TCase[int(pos.y/Var.dimCase),int(pos.x/Var.dimCase)]
    if(c.type == -1) :
        if pos.x -r < c.pos.x or pos.x + r > c.pos.x + Var.dimCase :
            individu.dpos.x *= -1
        if pos.y -r < c.pos.y or pos.y + r > c.pos.y + Var.dimCase :
            individu.dpos.y *= -1
    return
    
def rebond_bord(individu) :
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > Var.largeur*Var.dimCase:
        individu.dpos.x *= -1
    if pos.y - r < 0 or pos.y + r > Var.hauteur*Var.dimCase :
        individu.dpos.y *= -1
    return