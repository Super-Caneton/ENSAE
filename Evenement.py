from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import numpy as np
import Variables as Var
from Case import*
from Texte import*
from Ligne import*
from Individu import*
from Moteur import*


def nouveau(terrain) :
    if askyesno("Attention","Êtes vous sûr de vouloir tout supprimer ?"):
        terrain_vierge(terrain)
    return

#Sauvegarde
def enregistrer_sous():
    save = asksaveasfile(mode='w', filetypes=[('Fichier Texte (.txt)','.txt')], defaultextension=".txt")
    if save =="":
        return
    for x in range(Var.largeur) :
        for y in range(Var.hauteur-1) :
            save.write(str(Var.TCase[y,x].type)+" ")
        save.write(str(Var.TCase[Var.hauteur-1,x].type))
        save.write("\n")
    save.close()
    return

#Charge un terrain
def charger(terrain) :
    filename = askopenfilename(title="Ouvrir votre fichier",filetypes=[('Fichier Texte (.txt)','.txt')])
    if filename =="" :
        return
    terrain_vierge(terrain)
    save = open(filename, "r")
    data = save.readlines()
    for x, line in enumerate(data):
        L = line.split()
        for y,l in enumerate(L) :
            if(int(l)==1) :
                Var.LSortie.append([x,y])
            Var.TCase[y,x].type = int(l)
            Var.TCase[y,x].raffraichir()
    save.close()
    return
    
##

def remplir_mur() :
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.TCase[y,x].type = -1
            Var.TCase[y,x].raffraichir()
    return
    
##

def change_mode(nvmode):
    Var.mode = nvmode
    raffraichir()
    return
    
def affiche_grille() :
    Var.grilleTerrain = not(Var.grilleTerrain)
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            if(Var.grilleTerrain) :
                Var.TCase[y,x].grille = True
            else :
                Var.TCase[y,x].grille = False
    raffraichir()
    return
    
##

#Affiche des infos sur le programme
def info() :
    showinfo("A propos", Var.titre + " par LAM Kevin et MEILAC Adrien")
    return
    
##

def change_typePinceau(self):
    if(Var.typePinceau) :
        self.config(text = "Croix", command =  lambda : change_typePinceau(self))
    else :
        self.config(text = "Carré", command =  lambda : change_typePinceau(self))
    Var.typePinceau=not(Var.typePinceau)
    self.pack(fill=X)
    return
    
##

#Bouton Pause
def change_pause(self):
    Var.pause = not(Var.pause)
    if(Var.pause) :
        self.config(text = "Pause", command =  lambda : change_pause(self), relief = SUNKEN)
    else :
        self.config(text = "Pause", command =  lambda : change_pause(self), relief = RAISED)
    self.pack(fill=X)
    return


##

##Évènements

#Détermine quelle case est selectionnée selon les coordonnées du pointeur
def coordonnees_pointeur(x,y) :
    if (Var.xPointeur == x // Var.dimCase and Var.yPointeur == y // Var.dimCase) :
        Var.nvCase = False
    else :
        Var.nvCase = True
    Var.xPointeur = x // Var.dimCase
    Var.yPointeur = y // Var.dimCase
    return

def clic_gauche(event, taille_pinceau):
    coordonnees_pointeur(event.x,event.y)
    if(Var.typeCase!=1) :
        wavefront(Var.xPointeur,Var.yPointeur, [], [change_case_action], taille_pinceau.get(), Var.typePinceau)
    else :
        creer_sortie(Var.xPointeur,Var.yPointeur)
    return

def deplacement_clic_gauche(event, taille_pinceau) :
    coordonnees_pointeur(event.x,event.y)
    if(Var.nvCase) :
        if(Var.typeCase!=1) :
            wavefront(Var.xPointeur,Var.yPointeur, [], [change_case_action], taille_pinceau.get(), Var.typePinceau)
        else :
            creer_sortie(Var.xPointeur,Var.yPointeur)
    return
    
def efface_case(x,y):
    if(Var.TCase[y,x].type == 1) :
        Var.LSortie.remove([C.x,C.y])
    Var.TCase[y,x].score = -1
    Var.TCase[y,x].type = 0
    Var.TCase[y,x].raffraichir()
    
def clic_droit(event):
    coordonnees_pointeur(event.x,event.y)
    efface_case(Var.xPointeur,Var.yPointeur)
    return

def deplacement_clic_droit(event) :
    coordonnees_pointeur(event.x,event.y)
    if(Var.nvCase) :
        efface_case(Var.xPointeur,Var.yPointeur)
    return

#Remet toutes les valeurs par défaut
def reset_clic(event):
    Var.xPointeur = -1
    Var.yPointeur = -1
    Var.nvCase = False
    return

#Selestionne le type de case à appliquer
def selection(event):
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    if (value == "Mur") :
        Var.typeCase = -1
    elif (value == "Effacer") :
        Var.typeCase = 0
    elif (value == "Sortie") :
        Var.typeCase = 1
    return