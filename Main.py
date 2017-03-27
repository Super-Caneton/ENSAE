from tkinter import *
from Class import *
from math import *

##Variables

#Variable de la fenêtre
Titre="Projet d'info (Test)"
largeur=800
hauteur=500

TpsRaffraichissement=10 #Temps de raffraichissement en ms

#Variables concernant les individus
LIndiv=[]
NIndiv=20
rIndiv=5
mIndiv=1

#Coefficient de rebond elastique
eIndiv = 1
eMur = 1
eBord = 1

##GUI

#Fenêtre
tk = Tk()
tk.title(Titre)
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)

#Le terrain
terrain = Canvas(tk, width=largeur,height=hauteur, bd=0, highlightthickness=0, background="ivory")
terrain.pack()

tk.update()

###Méthodes

def init_indiv():
    for i in range(NIndiv) :
        pos = randvect2D(rIndiv, largeur-rIndiv,rIndiv, hauteur-rIndiv)
        dpos = randvect2D(-3,3,-3,3)
        indiv=individu(pos, dpos, rIndiv, mIndiv, terrain,"black")
        LIndiv.append(indiv)
    return


def bouge_indiv(individu) :
    individu.pos += individu.dpos
    terrain.move(individu.id, individu.dpos.x, individu.dpos.y)
    return


##Fonctions auxiliaires
def touche_indiv(individu1, individu2) :
    return (individu1.pos - individu2.pos).norme() <= individu1.r+individu2.r

def p_scal(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.x + vecteur1.y * vecteur2.y
    
def projection(vecteur1, vecteur2): #projection du vecteur "vecteur1" sur le vecteur "vecteur2"
    return p_scal(vecteur1, vecteur2) * vecteur2


##Gestion des rebonds
def rebond_indiv(individu1, individu2, e) : 

    n = individu1.pos - individu2.pos
    n *= 1/n.norme()
    
    n1 = projection(individu1.dpos, n)
    n2 = projection(individu2.dpos, n)
    
    t1 = individu1.dpos - n1
    t2 = individu2.dpos - n2
    
    individu1.dpos = t1 + n2*e
    individu2.dpos = t2 + n1*e
    
    return
    
def rebond_mur(individu, mur, e) :
    return
    
def rebond_bord(individu, e) :
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > largeur:
        individu.dpos.x *= -e
    if pos.y - r < 0 or pos.y + r > hauteur :
        individu.dpos.y *= -e
    return
    
##Forces
#Exemple d'application de forces
def gravitation(individu) :
    individu.dpos.y += 0.1
    return
    
def force_centrale(individu, pos, k, alpha) :
    om = (individu.pos - pos)
    individu.dpos -= k/(om.norme()**alpha)*om
    return


##Fonction de mise à jour
def update():
    for i, individu1 in enumerate(LIndiv) :
        bouge_indiv(individu1)
        rebond_bord(individu1,eBord)
        #force_centrale(individu1, vect2D(400,250), 0.001, 0)
        for individu2 in LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1,individu2, eIndiv)
                
    tk.update_idletasks()
    tk.after(TpsRaffraichissement, update)


##Initialisation
init_indiv()
tk.after(TpsRaffraichissement, update)
tk.mainloop()
