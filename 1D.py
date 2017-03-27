from tkinter import *
from random import *


##Variables
case = 100 #Longueur en nombre de case du chemin
taille_case = 10
NIndiv = 10
vlim = 6 #Vitesse limite des individus
r=3
LIndiv=[]
Lpos = [] #Liste de positions initiales des individus

Titre = "Projet d'info 1D"
largeur=case*taille_case
hauteur=100


##GUI
tk = Tk()
tk.title(Titre)
tk.resizable(0, 0)

terrain = Canvas(tk, width=largeur,height=hauteur, bd=0, highlightthickness=0, background="ivory")
terrain.pack(side=LEFT)

Button(tk, text ='Avancer', command=update).pack(side=RIGHT, padx=5, pady=5)

tk.update()


##Classe
class individu :
    def __init__(self, pos, dpos, r, canvas) :
        self.pos = pos
        self.dpos = dpos
        self.r = r
        self.canvas = canvas
        self.id = canvas.create_oval(-1*r, -1*r, r, r, fill="black")
        self.canvas.move(self.id, pos*taille_case, 50)
        
    def dessine(self) :
        self.canvas.move(self.id, self.dpos*taille_case, 0)


##Méthodes
def init_indiv():
    while len(LIndiv) < NIndiv:
        pos = randint(0, case - 1)
        dpos = randint(1, vlim)
        if pos not in Lpos :
            indiv = individu(pos, dpos, r, terrain)
            LIndiv.append(indiv)

def tri_indiv() :
    L=[] 
    for individu1 in LIndiv :
        flag=True
        for i, individu2 in enumerate(L) :
            if individu1.pos > individu2.pos :
                L = L[:i] + [individu1] + L[i:]
                flag=False
                break
        if(flag) :
            L.append(individu1)
    return L



## Fonction de mise à jour
def update():
    if len(LIndiv)>0 :
        #On déplace les individu "tous en même temps" et on fait sortir ceux qui sont au bout
        for individu in reversed(LIndiv):
            individu.pos += individu.dpos
            if individu.pos > case :
                terrain.delete(individu.id)
                LIndiv.remove(individu)
        #On ajuste la position des individus si certains dépassent ceux qui sont devant eux
        n = len(LIndiv)
        for i in reversed(range(n)) :
            if i < n - 1 :
                if LIndiv[i].pos > LIndiv[i+1].pos :
                    LIndiv[i].pos = LIndiv[i+1].pos - 1
            LIndiv[i].dessine()
        #tk.update_idletasks()
        #tk.after(1000, update)
    else :
        print("Fini !!!")


##Initialisation
init_indiv()
LIndiv=tri_indiv()
#tk.after(1000, update)
tk.mainloop()
