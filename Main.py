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
NIndiv=10
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
    dx=individu1.pos.x-individu2.pos.x
    dy=individu1.pos.y-individu2.pos.y
    d=sqrt(dx**2+dy**2)
    return d <= individu1.r+individu2.r
    
def p_scal(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.x + vecteur1.y * vecteur2.y
    
def projection(vecteur1, vecteur2): #projection du vecteur "self" sur le vecteur "vecteur"
    return vecteur1 - p_scal(vecteur1, vecteur2) * vecteur2


##Gestion des rebonds
def rebond_indiv(individu1, individu2, e) : 
    return
    
#def rebond_mur(individu, mur, e) :
    
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


##Fonction de mise à jour
def update():
    for i, individu1 in enumerate(LIndiv) :
        bouge_indiv(individu1)
        rebond_bord(individu1,eBord)
        for individu2 in LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1,individu2, eIndiv)
                
    tk.update_idletasks()
    tk.after(TpsRaffraichissement, update)


##Initialisation
init_indiv()
tk.after(TpsRaffraichissement, update)
tk.mainloop()
