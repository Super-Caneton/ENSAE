## Fichier Moteur.py
## Gère le fonctionnement de la simulation de mouvement de foule

import numpy as np
from Vect2D import *
import Variables as Var
from Case import *
from Texte import *
from Ligne import *
from Individu import *


def terrain_vierge(terrain):
    '''Cree un terrain vierge'''
    supprime_indiv(terrain)
    cacher_ligne()
    cacher_texte()
    Var.LSortie = []
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.TCase[y, x].type = 0
            Var.TCase[y, x].score = -1
            Var.TCase[y, x].raffraichir()
            Var.Tdirection[y, x].x = 0
            Var.Tdirection[y, x].y = 0
    return
    
def creer_sortie(x, y):
    '''Permet de declarer une case comme etant une sortie'''
    if not([x, y] in Var.LSortie): 
        change_case_action(vect2D(x, y))
        Var.LSortie.append([x, y])
    return
    
###Fonctions sur les statistiques :
def stat_dMaxCase(label) :
    '''Permet de mettre à jour la distance de la case la plus éloignée de la sortie'''
    Var.dMaxCase =-1
    infini = False
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            if(not(infini)) :
                if(Var.TCase[y,x].type ==0):
                    if(Var.TCase[y,x].score==-1) :
                        infini = True
                    elif(Var.TCase[y,x].score > Var.dMaxCase) :
                        Var.dMaxCase = Var.TCase[y,x].score
    if Var.dMaxCase == -1 :
        label.config(text = "∞")
    else :
        label.config(text = str(Var.dMaxCase))
    label.pack()
    return

def stat_nbIndiv(label):
    '''Permet de mettre à jour le nombre d'individus encore sur le terrain'''
    label.config(text = str(len(Var.LIndiv)))
    label.pack()
    return

##Moteur : Potential Field


##Conditions pour la fonction voisins prenant en argument un vect2D
#C : coordonnées de la forme vect2D(x,y)

def pas_mur_condition(C):
    '''boleen qui renvoit vrai si la case n'est pas un mur'''
    return (Var.TCase[C.y, C.x].type != -1)
    
##Actions pour la fonction voisins prenant en argument un vect2D et un int

def change_distance_action(C, d):
    '''Atribue une distance en fonction de d à la case C'''
    if Var.TCase[C.y, C.x].score >= 0 :
        Var.TCase[C.y, C.x].score = min(d, Var.TCase[C.y, C.x].score)
    else :
        Var.TCase[C.y, C.x].score = d
    return 
    
def augmente_distance_action(C, d = 0): #Inutilisée
    '''Ajoute une distance arbitraire à la case C'''
    if Var.TCase[C.y, C.x].score > 0 :
        Var.TCase[C.y, C.x].score += 10
    return
    
def change_case_action(C, d = 0):
    '''Change le type de case de la case C'''
    if(Var.TCase[C.y, C.x].type == 1) :
        Var.LSortie.remove([C.x, C.y])
    Var.TCase[C.y, C.x].score = -1
    Var.TCase[C.y, C.x].type = Var.typeCase
    Var.TCase[C.y, C.x].raffraichir()
    return


##
def voisins(x, y, Lcondition, t):
    '''Renvoie la liste des voisins de la case (x,y) qui satisfont une liste de conditions'''
    #t=False : voisin de Von Neumann
    #t=True : Voisin de Moore
    L = []
    V = [vect2D(x - 1, y), vect2D(x + 1, y), vect2D(x, y - 1), vect2D(x, y + 1)]
    if(t) :
        V= V + [vect2D(x - 1,y - 1), vect2D(x - 1,y + 1), vect2D(x + 1,y - 1), vect2D(x + 1,y + 1)]
    for C in V : # C : coordonnees de la forme vect2D(x,y)
        
        if 0 <= C.x and C.x < Var.largeur and 0 <= C.y and C.y < Var.hauteur: # Verifie que le voisin est dans le domaine du terrain
            if(Var.TCase[C.y, C.x].explore == False) : # Verifie que la case n'a pas deja ete exploree
                flag = True
                for condition in Lcondition : # On verifie que le voisin verifie toutes les conditions
                    if not(condition(C)) :
                        flag = False
                        break
                if(flag): # Si c'est le cas, on l'ajoute a la liste des voisins disponibles
                    L.append(C)
                    Var.TCase[C.y, C.x].explore = True
    return L

def reset_case():
    '''Remarque les cases comme inexplorees, utile pour reparcourir les cases'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.TCase[y, x].explore = False
    return

##
def wavefront(x, y, Lcondition, Laction, maxd, t):
    '''Algorithme WaveFront, point de départ (x,y), Choisit les voisins selon Lcondition et leur applique Laction dans un rayon maxd'''
    #x,y coordonnées de la case de départ
    #t=False : voisin de Von Neumann
    #t=True : Voisin de Moore
    d=0
    L=[vect2D(x, y)]
    while d < maxd and len(L) != 0 :
        V = []
        for C in L : #C : coordonnées de la forme vect2D(x,y)
            V = V + voisins(C.x, C.y, Lcondition, t)
            for action in Laction :
                action(C, d)
        d += 1
        L = []
        for v in V :
            L.append(v)
    reset_case()
    return

def recalcule_champ_potentiel():
    '''Recalcule le champ de potentiel'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            Var.TCase[y, x].score = -1
    for S in Var.LSortie :
        wavefront(S[0], S[1], [pas_mur_condition], [change_distance_action], Var.hauteur * Var.largeur, False)
    direction()
    raffraichir()
    return
    
##
def direction() :
    '''Calcule le tableau des directions à prendre'''
    for x in range(Var.largeur):
        for y in range(Var.hauteur):
            if(Var.TCase[y, x].score != -1):
                V = voisins(x, y, [pas_mur_condition], False)
                reset_case()
                #On va calculer le vecteur à prendre : le gradient de distance
                
                #Fonctions auxiliaires
                def aux1():
                    s = Var.TCase[y, x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if Var.TCase[v.y, v.x].score < s :
                            vx = vx + v.x-x
                            vy = vy + v.y-y
                    return (vx, vy)
                def aux2():
                    s = Var.TCase[y, x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if Var.TCase[v.y, v.x].score < s :
                            vx = v.x - x
                            vy = v.y - y
                    return (vx, vy)
                
                #Lorsqu'il n'y a pas de problème
                if len(V) == 4 :
                    vx = Var.TCase[y, x - 1].score - Var.TCase[y, x + 1].score
                    vy = Var.TCase[y - 1, x].score - Var.TCase[y + 1, x].score
                    #Évite aux individus de rester bloqués dans les coins
                    if Var.TCase[y + np.sign(vy), x + np.sign(vx)].type < 0 : 
                        (vx, vy) = aux2()
                elif len(V) == 2 :
                    #Problème de murs en coin
                    if abs(V[0].x - x) + abs(V[1].x - x) == 1 :
                        (vx, vy) = aux2()
                    else :
                        (vx, vy) = aux1()
                #Autre problème
                else :
                    (vx, vy) = aux1()
                if vect2D(vx, vy).norme() !=0 :
                    Var.Tdirection[y, x] = vect2D(vx, vy).normalise()
                else :
                    (vx, vy) = aux2()
                    if vect2D(vx,vy).norme() !=0 :
                        Var.Tdirection[y, x] = 1 / vect2D(vx, vy).norme() * vect2D(vx, vy)
                    else : 
                        Var.Tdirection[y, x] = vect2D(vx, vy)
                
    return
    
def raffraichir():
    '''Permet de raffraichir les cases et d'appliquer le dégradé correspondant à la distance du plus court chemin et les valeurs même de cette distance en chaque case en fonction du mode'''
    cacher_ligne()
    cacher_texte()
    if Var.mode == 1 : # mode 1 = aucun affichage
        for x in range(Var.largeur) :
            for y in range(Var.hauteur) :
                Var.TCase[y, x].raffraichir()
    if(Var.mode >= 2) : # mode 2 = on affiche uniquement un degradé
        fg = (10, 10, 100)
        bg = (255, 255, 255)
        for x in range(Var.largeur):
            for y in range(Var.hauteur):
                Var.TCase[y, x].raffraichir()
                if Var.TCase[y ,x].score > 0 :
                    Var.TCase[y, x].degrade(fg, bg, Var.hauteur + Var.largeur)
        if Var.mode == 3: # mode 3 = on affiche un dégradé et les valeurs des distances
            for x in range(Var.largeur):
                for y in range(Var.hauteur):
                    if(Var.TCase[y, x].score == -1):
                        Var.Ttexte[y, x].mot = "∞"
                    else :
                        Var.Ttexte[y, x].mot = str(Var.TCase[y, x].score)
                    Var.Ttexte[y, x].raffraichir()
        if Var.mode == 4: # mode 4 = on affiche un degradé et les vecteurs directionnels
            for x in range(Var.largeur):
                for y in range(Var.hauteur):
                    Var.Tligne[y, x].pos1 = vect2D(x,y) * Var.dimCase + vect2D(1,1) * (Var.dimCase / 2)
                    Var.Tligne[y, x].pos2 = Var.Tligne[y, x].pos1 + Var.Tdirection[y,x] * 5
                    Var.Tligne[y, x].raffraichir()
    return
