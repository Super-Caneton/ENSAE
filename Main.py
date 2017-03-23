from tkinter import *
from Class import *

##Variables
Titre="Projet d'info (Test)"
largeur=500
hauteur=400

TpsRaffraichissement=10 #Temps de raffraichissement en ms

LIndiv=[]
NIndiv=100
rIndiv=5
mIndiv=1

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

##Méthodes

def init_indiv():
    for i in range(NIndiv) :
        pos = randvect2D(rIndiv, largeur-rIndiv,rIndiv, hauteur-rIndiv)
        dpos = randvect2D(-3,3,-3,3)
        indiv=individu(pos, dpos, rIndiv, mIndiv, terrain,"black")
        LIndiv.append(indiv)
    return

def verif() :
    for i in LIndiv :
        bouge_indiv(i)
        rebond_bord(i,1)
    return

def bouge_indiv(individu) :
    individu.pos.x += individu.dpos.x
    individu.pos.y += individu.dpos.y
    #individu.pos += individu.dpos       #Problème concernant la surcharge d'opérateur
    individu.canvas.move(individu.id, individu.dpos.x, individu.dpos.y)
    return
    

##Gestion des rebonds
#e coefficient de rebond elastique
    #def rebond_indiv(individu1, individu2, eIndiv) : 
        
    #def rebond_mur(individu, mur, eMur) :
    
def rebond_bord(individu, eBord) :
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > largeur:
        individu.dpos.x *= -eBord
    if pos.y - r < 0 or pos.y + r > hauteur :
        individu.dpos.y *= -eBord
    return


##Fonction de mise à jour
def update():
    verif()
    tk.update_idletasks()
    tk.after(TpsRaffraichissement, update)


##Initialisation
init_indiv()
tk.after(TpsRaffraichissement, update)
tk.mainloop()
