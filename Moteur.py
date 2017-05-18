from Vect2D import*
import numpy as np
import Variables as Var
from Case import*
from Texte import*
from Ligne import*
from Individu import*


#Crée un terrain vierge
def terrain_vierge(terrain) :
    supprime_indiv(terrain)
    cacher_ligne()
    cacher_texte()
    Var.LSortie=[]
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.TCase[y,x].type = 0
            Var.TCase[y,x].score = -1
            Var.TCase[y,x].raffraichir()
            Var.Tdirection[y,x].x = 0
            Var.Tdirection[y,x].y = 0
    return
    
def creer_sortie(x,y) :
    if not([x,y] in Var.LSortie) :
        change_case_action(vect2D(x,y))
        Var.LSortie.append([x,y])
    return

##Moteur : Potential Field


##Conditions pour la fonction voisins prenant en argument un vect2D
#C : coordonnées de la forme vect2D(x,y)

def pas_mur_condition(C):
    return (Var.TCase[C.y,C.x].type != -1)
    
##Actions pour la fonction voisins prenant en argument un vect2D et un int

def change_distance_action(C,d):
    if Var.TCase[C.y,C.x].score >= 0 :
        Var.TCase[C.y,C.x].score = min(d, Var.TCase[C.y,C.x].score)
    else :
        Var.TCase[C.y,C.x].score = d
    return 
    
def augmente_distance_action(C, d=0) :
    if Var.TCase[C.y,C.x].score > 0 :
        Var.TCase[C.y,C.x].score +=10
    return
    
def change_case_action(C, d=0):
    if(Var.TCase[C.y,C.x].type == 1) :
        Var.LSortie.remove([C.x,C.y])
    Var.TCase[C.y,C.x].score = -1
    Var.TCase[C.y,C.x].type = Var.typeCase
    Var.TCase[C.y,C.x].raffraichir()
    return


##
#Renvoie la liste des voisins de (x,y) qui satisfont les conditions de la liste "Lcondition"
#t=False : voisin de Von Neumann
#t=True : Voisin de Moore
def voisins(x,y, Lcondition, t):
    L=[]
    V=[vect2D(x-1,y),vect2D(x+1,y),vect2D(x,y-1),vect2D(x,y+1)]
    if(t) :
        V= V + [vect2D(x-1,y-1), vect2D(x-1,y+1), vect2D(x+1,y-1), vect2D(x+1,y+1)]
    for C in V : #C : coordonnées de la forme vect2D(x,y)
        #Vérifie que le voisin existe bien
        if 0 <= C.x and C.x < Var.largeur :
            if 0 <= C.y and C.y < Var.hauteur :
                #Vérifie que la case n'a pas déjà été explorée
                if(Var.TCase[C.y,C.x].explore == False) : 
                    flag=True
                    #Vérifie toutes les conditions du voisin
                    for condition in Lcondition :
                        if not(condition(C)) :
                            flag=False
                    if(flag):
                        L.append(C)
                        Var.TCase[C.y,C.x].explore = True
    return L

#Remarque les cases comme inexplorées
def reset_case() :
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.TCase[y,x].explore = False
    return

##Algorithme WaveFront
#Point de départ (x,y), Choisit les voisins selon Lcondition et leur applique Laction dans un rayon maxd
#t=False : voisin de Von Neumann
#t=True : Voisin de Moore
def wavefront(x,y, Lcondition, Laction, maxd, t): #x,y coordonnées de la case de départ
    d=0
    L=[vect2D(x,y)]
    while d < maxd and len(L) != 0 :
        V = []
        for C in L : #C : coordonnées de la forme vect2D(x,y)
            V = V + voisins(C.x, C.y, Lcondition, t)
            for action in Laction :
                action(C,d)
        d = d+1
        L = []
        for v in V :
            L.append(v)
    reset_case()
    return

##
#Recalcule le champ de potentiel
def recalcule_champ_potentiel() :
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            Var.TCase[y,x].score = -1
    for S in Var.LSortie :
        wavefront(S[0],S[1], [pas_mur_condition], [change_distance_action], Var.hauteur*Var.largeur, False)
    direction()
    raffraichir()
    return
    
    
#A MODIFIER <======================================
#Calcule le tableau des directions à prendre
def direction() :
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            if(Var.TCase[y,x].score != -1):
                V=voisins(x,y,[pas_mur_condition], False)
                reset_case()
                #On va calculer le vecteur à prendre : le gradient de distance
                def aux1():
                    s=Var.TCase[y,x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if Var.TCase[v.y, v.x].score < s :
                            vx = vx + v.x-x
                            vy = vy + v.y-y
                    return (vx,vy)
                def aux2():
                    s=Var.TCase[y,x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if Var.TCase[v.y, v.x].score < s :
                            vx = v.x-x
                            vy = v.y-y
                    return (vx,vy)
                #Lorsqu'il n'y a pas de problème
                if len(V)==4 :
                    vx = Var.TCase[y,x-1].score - Var.TCase[y,x+1].score
                    vy = Var.TCase[y-1,x].score - Var.TCase[y+1,x].score
                    #Évite aux individus de rester bloqués dans les coins
                    if Var.TCase[y+np.sign(vy),x+np.sign(vx)].type < 0 : 
                        (vx,vy)=aux2()
                elif len(V)==2 :
                    #Problème de murs en coin
                    if (abs(V[0].x-x)+abs(V[1].x-x)==1) :
                        (vx,vy) = aux2()
                    else :
                        (vx,vy) = aux1()
                #Autre problème
                else :
                    (vx,vy) = aux1()
                if(vect2D(vx,vy).norme() !=0):
                    Var.Tdirection[y,x] = vect2D(vx,vy).normalise()
                else :
                    (vx,vy) = aux2()
                    if(vect2D(vx,vy).norme() !=0):
                        Var.Tdirection[y,x] = 1/vect2D(vx,vy).norme()*vect2D(vx,vy)
                    else : 
                        Var.Tdirection[y,x] = vect2D(vx,vy)
                
    return
    
##
#Application du dégradé pour le champ de potentiel
def raffraichir():
    cacher_ligne()
    cacher_texte()
    if(Var.mode == 1) :
        for x in range(Var.largeur) :
            for y in range(Var.hauteur) :
                Var.TCase[y,x].raffraichir()
    if(Var.mode >= 2) :
        fg = (10,10,100)
        bg = (255,255,255)
        for x in range(Var.largeur) :
            for y in range(Var.hauteur) :
                Var.TCase[y,x].raffraichir()
                if Var.TCase[y,x].score > 0 :
                    Var.TCase[y,x].degrade(fg, bg, Var.hauteur+Var.largeur)
        if(Var.mode==3) :
            for x in range(Var.largeur) :
                for y in range(Var.hauteur) :
                    if(Var.TCase[y,x].score==-1):
                        Var.Ttexte[y,x].mot = "∞"
                    else :
                        Var.Ttexte[y,x].mot = str(Var.TCase[y,x].score)
                    Var.Ttexte[y,x].raffraichir()
        if(Var.mode==4) :
            for x in range(Var.largeur) :
                for y in range(Var.hauteur) :
                    Var.Tligne[y,x].pos1 = vect2D(x,y)*Var.dimCase+vect2D(1,1)*(Var.dimCase/2)
                    Var.Tligne[y,x].pos2 = Var.Tligne[y,x].pos1+Var.Tdirection[y,x]*5
                    Var.Tligne[y,x].raffraichir()
    return