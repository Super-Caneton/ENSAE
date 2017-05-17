from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from Class import *
#import math
import numpy as np
import random as rd

#REMARQUE : Le code s'apparente de plus en plus a du spaghetti code : a retravailler

#A Faire
#Ajouter les collisions entre individus OK
#Système de sauvegarde OK
#Pinceau pour individus
#Autres intéractions entre individus
#Eclaircir le code
#Statistiques
#Optimisation
#Esthétique (mvt fluide + interface utilisateur) OK

##Variables

#Rappel : x = abscisse, y = ordonnée, (0,0) en haut à gauche

#Variable de la fenêtre
titre="Simulateur de foule from scratch"
largeur=50
hauteur=30

TpsRaffraichissement=10 #Temps de raffraichissement en ms

#Variables relatif à la selection des cases

#Coordonnées de la case selectionnée (-1,-1) si aucune
xPointeur = -1
yPointeur = -1

nvCase = True #Détermine si on a selectionné une nouvelle case
typeCase = 0

#False : Voisin de Von Neumann => Croix
#True : Voisin de Moore => Carré
typePinceau = False

#Variables concernant les cases
TCase = np.array([],case) #Pour demander la case à la xième colonne, yième ligne écrire TCase[y,x]
Tdirection = np.array([[vect2D()]*largeur]*hauteur,vect2D) #Tableau des vecteur direction
Tligne = np.array([],ligne)
Ttexte = np.array([],texte)
dimCase = 20 #Taille de la case en pixels

#Variables concernant les sorties 
LSortie = [] #objets de la forme [x,y]

#Variables concernant les individus
LIndiv=[]
NIndiv=100
rIndiv=5
vminIndiv=0.5
vmaxIndiv=2

pause = False #Met en pause le mouvement des individus
grilleTerrain = False

#Statistique
dMaxCase=-1 #Distance maximale d'une case d'une sortie

###Méthodes

##Fonctions auxiliaires
    
def touche_indiv(individu1, individu2) :
    return (individu1.pos - individu2.pos).norme() <= individu1.r+individu2.r

def p_scal(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.x + vecteur1.y * vecteur2.y
    
def projection(vecteur1, vecteur2): #projection du vecteur "vecteur1" sur le vecteur "vecteur2"
    return p_scal(vecteur1, vecteur2.normalise())*vecteur2.normalise()


##Fonctions sur les individus

#Initialisation des individus
def init_indiv():
    supprime_indiv()
    for i in range(NIndiv) :
        x = uniform(rIndiv, (largeur-1)*dimCase-rIndiv)
        y = uniform(rIndiv, (hauteur-1)*dimCase-rIndiv)
        while TCase[int(y/dimCase),int(x/dimCase)].type < 0 :
            x = uniform(rIndiv, (largeur-1)*dimCase-rIndiv)
            y = uniform(rIndiv, (hauteur-1)*dimCase-rIndiv)
        pos = vect2D(x,y)
        dpos = vect2D(0,0)
        indiv=individu(pos, dpos, rIndiv, terrain,"red")
        LIndiv.append(indiv)
    return

def supprime_indiv() :
    global LIndiv
    for i in LIndiv :
        terrain.delete(i.id)
    LIndiv = []
    return
    
def sortir_indiv() :
    for individu in LIndiv :
        x=int(individu.pos.x/dimCase)
        y=int(individu.pos.y/dimCase)
        if(TCase[y,x].type==1) :
            terrain.delete(individu.id)
            LIndiv.remove(individu)
    return
    
def bouge_indiv() :
    for i, individu1 in enumerate(LIndiv) :
        x=int(individu1.pos.x/dimCase)
        y=int(individu1.pos.y/dimCase)
        individu1.dpos += Tdirection[y,x]
        for individu2 in LIndiv[i+1:] :
            if touche_indiv(individu1, individu2) :
                rebond_indiv(individu1,individu2)
        rebond_bord(individu1)
        rebond_mur(individu1)
        individu1.dpos = individu1.dpos.normalise()*uniform(vminIndiv,vmaxIndiv)
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
    c = TCase[int(pos.y/dimCase),int(pos.x/dimCase)]
    if(c.type == -1) :
        if pos.x -r < c.pos.x or pos.x + r > c.pos.x + dimCase :
            individu.dpos.x *= -1
        if pos.y -r < c.pos.y or pos.y + r > c.pos.y + dimCase :
            individu.dpos.y *= -1
    return
    
def rebond_bord(individu) :
    pos = individu.pos
    r = individu.r
    if pos.x -r < 0 or pos.x + r > largeur*dimCase:
        individu.dpos.x *= -1
    if pos.y - r < 0 or pos.y + r > hauteur*dimCase :
        individu.dpos.y *= -1
    return
    
    
##Moteur : Potential Field


#Conditions pour la fonction voisins prenant en argument un vect2D
#C : coordonnées de la forme vect2D(x,y)

def pas_mur_condition(C):
    return (TCase[C.y,C.x].type != -1)
    
#Actions pour la fonction voisins prenant en argument un vect2D et un int

def change_distance_action(C,d):
    if TCase[C.y,C.x].score >= 0 :
        TCase[C.y,C.x].score = min(d, TCase[C.y,C.x].score)
    else :
        TCase[C.y,C.x].score = d
    return 
    
def augmente_distance_action(C, d=0) :
    if TCase[C.y,C.x].score > 0 :
        TCase[C.y,C.x].score +=10
    return
    
def change_case_action(C, d=0):
    if(TCase[C.y,C.x].type == 1) :
        LSortie.remove([C.x,C.y])
    TCase[C.y,C.x].score = -1
    TCase[C.y,C.x].type = typeCase
    TCase[C.y,C.x].raffraichir()
    return

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
        if 0 <= C.x and C.x < largeur :
            if 0 <= C.y and C.y < hauteur :
                #Vérifie que la case n'a pas déjà été explorée
                if(TCase[C.y,C.x].explore == False) : 
                    flag=True
                    #Vérifie toutes les conditions du voisin
                    for condition in Lcondition :
                        if not(condition(C)) :
                            flag=False
                    if(flag):
                        L.append(C)
                        TCase[C.y,C.x].explore = True
    return L

#Remarque les cases comme inexplorées
def reset_case() :
    for x in range(largeur) :
        for y in range(hauteur) :
            TCase[y,x].explore = False
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
    
    
##Fonction sur le terrain

#Initialisation des cases
def init_case() :
    global TCase
    TCase = np.array([[case(canvas=terrain)]*largeur]*hauteur,case)
    for x in range(largeur) :
        for y in range(hauteur) :
            pos=vect2D(x,y)
            c = case(pos, dimCase, 0, -1, terrain, "ivory", False)
            TCase[y,x]=c
    return
    
#Crée un terrain vierge
def terrain_vierge() :
    global LSortie
    supprime_indiv()
    cacher_ligne()
    cacher_texte()
    LSortie=[]
    for x in range(largeur) :
        for y in range(hauteur) :
            TCase[y,x].type = 0
            TCase[y,x].score = -1
            TCase[y,x].raffraichir()
            Tdirection[y,x].x = 0
            Tdirection[y,x].y = 0
    
    stat_dMaxCase()
    stat_nbIndiv()
    return

#Application du dégradé pour le champ de potentiel
def applique_degrade():
    cacher_ligne()
    cacher_texte()
    if(mode == 1) :
        for x in range(largeur) :
            for y in range(hauteur) :
                TCase[y,x].raffraichir()
    if(mode >= 2) :
        fg = (10,10,100)
        bg = (255,255,255)
        for x in range(largeur) :
            for y in range(hauteur) :
                if TCase[y,x].score > 0 :
                    TCase[y,x].degrade(fg, bg, hauteur+largeur)
        if(mode==3) :
            for x in range(largeur) :
                for y in range(hauteur) :
                    if(TCase[y,x].score==-1):
                        Ttexte[y,x].mot = "∞"
                    else :
                        Ttexte[y,x].mot = str(TCase[y,x].score)
                    Ttexte[y,x].raffraichir()
        if(mode==4) :
            for x in range(largeur) :
                for y in range(hauteur) :
                    Tligne[y,x].pos1 = vect2D(x,y)*dimCase+vect2D(1,1)*(dimCase/2)
                    Tligne[y,x].pos2 = Tligne[y,x].pos1+Tdirection[y,x]*5
                    Tligne[y,x].raffraichir()
    return
    
##Affichage des vecteurs
def init_ligne():
    global Tligne
    Tligne=np.array([[ligne(canvas=terrain)]*largeur]*hauteur,ligne)
    for x in range(largeur) :
        for y in range(hauteur) :
            Tligne[y,x]=ligne(canvas=terrain)
    return
    
def cacher_ligne() :
    for x in range(largeur) :
        for y in range(hauteur) :
            Tligne[y,x].pos1 = vect2D()
            Tligne[y,x].pos2 = vect2D()
            Tligne[y,x].raffraichir()
    return
    
##Affichage des distances
def init_texte():
    global Ttexte
    Ttexte=np.array([[texte(canvas=terrain)]*largeur]*hauteur,texte)
    for x in range(largeur) :
        for y in range(hauteur) :
            Ttexte[y,x]=texte(vect2D(x,y)*dimCase+vect2D(1,1)*(dimCase/2), canvas=terrain)
    return
    
def cacher_texte() :
    for x in range(largeur) :
        for y in range(hauteur) :
            Ttexte[y,x].mot = ""
            Ttexte[y,x].raffraichir()
    return

#Recalcule le champ de potentiel
def recalcule_champ_potentiel() :
    for x in range(largeur) :
        for y in range(hauteur) :
            TCase[y,x].score = -1
    for S in LSortie :
        wavefront(S[0],S[1], [pas_mur_condition], [change_distance_action], hauteur*largeur, False)
    direction()
    applique_degrade()

    stat_dMaxCase()
    return
    
    
#A MODIFIER <======================================
#Calcule le tableau des directions à prendre
def direction() :
    for x in range(largeur) :
        for y in range(hauteur) :
            if(TCase[y,x].score != -1):
                V=voisins(x,y,[pas_mur_condition], False)
                reset_case()
                #On va calculer le vecteur à prendre : le gradient de distance
                def aux1():
                    s=TCase[y,x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if TCase[v.y, v.x].score < s :
                            vx = vx + v.x-x
                            vy = vy + v.y-y
                    return (vx,vy)
                def aux2():
                    s=TCase[y,x].score
                    vx = 0
                    vy = 0
                    for v in V :
                        if TCase[v.y, v.x].score < s :
                            vx = v.x-x
                            vy = v.y-y
                    return (vx,vy)
                #Lorsqu'il n'y a pas de problème
                if len(V)==4 :
                    vx = TCase[y,x-1].score - TCase[y,x+1].score
                    vy = TCase[y-1,x].score - TCase[y+1,x].score
                    #Évite aux individus de rester bloqués dans les coins
                    if TCase[y+np.sign(vy),x+np.sign(vx)].type < 0 : 
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
                    Tdirection[y,x] = vect2D(vx,vy).normalise()
                else :
                    (vx,vy) = aux2()
                    if(vect2D(vx,vy).norme() !=0):
                        Tdirection[y,x] = 1/vect2D(vx,vy).norme()*vect2D(vx,vy)
                    else : 
                        Tdirection[y,x] = vect2D(vx,vy)
                
    return
    
#Créer une sortie en (x,y)
def creer_sortie(x,y) :
    if not([x,y] in LSortie) :
        change_case_action(vect2D(x,y))
        LSortie.append([x,y])
    return
    
###Fonctions sur les statistiques :
def stat_dMaxCase() :
    global dMaxCase
    dMaxCase =-1
    infini = False
    for x in range(largeur) :
        for y in range(hauteur) :
            if(not(infini)) :
                if(TCase[y,x].type ==0):
                    if(TCase[y,x].score==-1) :
                        infini = True
                    elif(TCase[y,x].score > dMaxCase) :
                        dMaxCase = TCase[y,x].score
    if dMaxCase == -1 :
        label_dMaxCase.config(text = "∞")
    else :
        label_dMaxCase.config(text = str(dMaxCase))
    label_dMaxCase.pack()
    return

def stat_nbIndiv():
    label_nbIndiv.config(text = str(len(LIndiv)))
    label_nbIndiv.pack()
    return
    
###GUI

#Fenêtre
tk = Tk()
tk.title(titre)
tk.resizable(0, 0)
#tk.wm_attributes("-topmost", 1)

#Panneau de délimitation gloable
p = PanedWindow(tk, orient=HORIZONTAL)
p.pack()

#Panneau de délimitation à gauche
p1 = PanedWindow(p, orient=VERTICAL)
p1.pack(side = LEFT, fill=Y)

#Panneau de délimitation en bas
p2 = PanedWindow(p, orient=HORIZONTAL)
p2.pack(side = RIGHT, fill=Y)

##Menu
menubar = Menu(tk)


def nouveau() :
    global LSortie
    if askyesno("Attention","Êtes vous sûr de vouloir tout supprimer ?"):
        terrain_vierge()
    return
 
#Affiche des infos sur le programme
def info() :
    showinfo("A propos", titre + " par LAM Kevin et MEILAC Adrien")
    return

#Sauvegarde
def enregistrer_sous():
    save = asksaveasfile(mode='w', filetypes=[('Fichier Texte (.txt)','.txt')], defaultextension=".txt")
    if save =="":
        return
    for x in range(largeur) :
        for y in range(hauteur-1) :
            save.write(str(TCase[y,x].type)+" ")
        save.write(str(TCase[hauteur-1,x].type))
        save.write("\n")
    save.close()
    return

#Charge un terrain
def charger() :
    filename = askopenfilename(title="Ouvrir votre fichier",filetypes=[('Fichier Texte (.txt)','.txt')])
    if filename =="" :
        return
    terrain_vierge()
    save = open(filename, "r")
    data = save.readlines()
    for x, line in enumerate(data):
        L = line.split()
        for y,l in enumerate(L) :
            if(int(l)==1) :
                LSortie.append([x,y])
            TCase[y,x].type = int(l)
            TCase[y,x].raffraichir()
    save.close()
    return
    

def remplir_mur() :
    for x in range(largeur) :
        for y in range(hauteur) :
            TCase[y,x].type = -1
            TCase[y,x].raffraichir()
    return
    
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau", command=nouveau)
menu1.add_command(label="Enregistrer sous...", command=enregistrer_sous)
menu1.add_command(label="Charger", command=charger)
menu1.add_separator()
menu1.add_command(label="Quitter", command=tk.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label= "Remplir de mur", command = remplir_mur)
menubar.add_cascade(label="Éditer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Manuel")
menu3.add_command(label="A propos", command=info)
menubar.add_cascade(label="Aide", menu=menu3)

tk.config(menu=menubar)

##Boite à outils
Label(p1, text = "Boite à outils").pack(side = TOP)
Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Pinceau
Label(p1, text = "Pinceau").pack()

# liste de sélection
liste = Listbox(p1)
liste.insert(1, "Mur")
liste.insert(2, "Sortie")
liste.insert(3, "Effacer")

liste.pack(fill=X)

#Taille du pinceau
Label(p1, text = "Taille du pinceau").pack()
taille_pinceau = Scale(p1,from_=1, to=10, orient=HORIZONTAL)
taille_pinceau.pack(fill=X)

def change_typePinceau():
    global typePinceau
    if(typePinceau) :
        bouton_typePinceau.config(text = "Croix", command = change_typePinceau)
    else :
        bouton_typePinceau.config(text = "Carré", command = change_typePinceau)
    typePinceau=not(typePinceau)
    bouton_typePinceau.pack(fill=X)
    return

#Type de pinceau
Label(p1, text = "Forme du pinceau").pack()
bouton_typePinceau = Button(p1, text = "Croix", command = change_typePinceau)
bouton_typePinceau.pack(fill=X)


def affiche_grille() :
    global grilleTerrain
    grilleTerrain = not(grilleTerrain)
    for x in range(largeur) :
        for y in range(hauteur) :
            if(grilleTerrain) :
                TCase[y,x].grille = True
            else :
                TCase[y,x].grille = False
    applique_degrade()
    return

bouton_grille = Button(p1, text = "Grille", command = affiche_grille)
bouton_grille.pack(fill=X)

Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

#Choix du mode
# 1 = Normal, 2 = Champ de potentiel
mode = 1

def change_mode():
    global mode
    if(mode==1) :
        mode = 2
        bouton_mode.config(text = "Champ de potentiel", command = change_mode)
    elif(mode==2) :
        mode=3
        bouton_mode.config(text = "Distance", command = change_mode)
    elif(mode==3) :
        mode=4
        bouton_mode.config(text = "Ligne de Champ", command = change_mode)
    else :
        mode = 1
        bouton_mode.config(text = "Normal", command = change_mode)
    applique_degrade()
    bouton_mode.pack(fill=X)
    return

Label(p1, text = "Selection du mode").pack()
bouton_mode = Button(p1, text = "Normal", command = change_mode)
bouton_mode.pack(fill=X)

bouton_recalcule = Button(p1, text = "Recalculer le champ", command = recalcule_champ_potentiel)
bouton_recalcule.pack(fill=X)


#Boutons relatifs aux individus
Frame(p1, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

Label(p1, text = "Individus").pack()

bouton_indiv = Button(p1, text = "Placer", command = init_indiv)
bouton_indiv.pack(fill=X)

bouton_indiv2 = Button(p1, text = "Supprimer", command = supprime_indiv)
bouton_indiv2.pack(fill=X)

#Bouton Pause
def change_pause():
    global pause
    pause = not(pause)
    if(pause) :
        bouton_pause.config(text = "Pause", command = change_pause, relief = SUNKEN)
    else :
        bouton_pause.config(text = "Pause", command = change_pause, relief = RAISED)
    bouton_pause.pack(fill=X)
    return

bouton_pause = Button(p1, text = "Pause", command = change_pause)
bouton_pause.pack(fill=X)

##Statistiques
Label(p2, text = "Statistiques").pack(side = TOP)
Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

Label(p2, text = "Distance du point\n le plus éloigné\n d'une sortie :").pack()
label_dMaxCase = Label(p2, text = "∞")
label_dMaxCase.pack()

Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

Label(p2, text = "Nombre\n d'individus :").pack()
label_nbIndiv = Label(p2, text = str(len(LIndiv)))
label_nbIndiv.pack()

Frame(p2, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)


##Le terrain
terrain = Canvas(p, width=largeur*dimCase,height=hauteur*dimCase, bd=0, highlightthickness=0, background="ivory")
terrain.pack(side=RIGHT)

tk.update()

##Évènements

#Détermine quelle case est selectionnée selon les coordonnées du pointeur
def coordonnees_pointeur(x,y) :
    global xPointeur, yPointeur, nvCase
    if (xPointeur == x // dimCase and yPointeur == y // dimCase) :
        nvCase = False
    else :
        nvCase = True
    xPointeur = x // dimCase
    yPointeur = y // dimCase
    return

def clic_gauche(event):
    coordonnees_pointeur(event.x,event.y)
    if(typeCase!=1) :
        wavefront(xPointeur,yPointeur, [], [change_case_action], taille_pinceau.get(), typePinceau)
    else :
        creer_sortie(xPointeur,yPointeur)
    return

def deplacement_clic_gauche(event) :
    coordonnees_pointeur(event.x,event.y)
    if(nvCase) :
        if(typeCase!=1) :
            wavefront(xPointeur,yPointeur, [], [change_case_action], taille_pinceau.get(), typePinceau)
        else :
            creer_sortie(xPointeur,yPointeur)
    return
    
def efface_case(x,y):
    if(TCase[y,x].type == 1) :
        LSortie.remove([C.x,C.y])
    TCase[y,x].score = -1
    TCase[y,x].type = 0
    TCase[y,x].raffraichir()
    
def clic_droit(event):
    coordonnees_pointeur(event.x,event.y)
    efface_case(xPointeur,yPointeur)
    return

def deplacement_clic_droit(event) :
    coordonnees_pointeur(event.x,event.y)
    if(nvCase) :
        efface_case(xPointeur,yPointeur)
    return

#Remet toutes les valeurs par défaut
def reset_clic(event):
    global xPointeur, yPointeur, nvCase
    xPointeur = -1
    yPointeur = -1
    nvCase = False
    return

#Selestionne le type de case à appliquer
def selection(event):
    global typeCase
    w = event.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    if (value == "Mur") :
        typeCase = -1
    elif (value == "Effacer") :
        typeCase = 0
    elif (value == "Sortie") :
        typeCase = 1
    return

#Evenements relatif au terrain
terrain.bind("<Button-1>", clic_gauche)
terrain.bind("<Button-3>", clic_droit)
terrain.bind("<B1-Motion>", deplacement_clic_gauche)
terrain.bind("<B3-Motion>", deplacement_clic_droit)
terrain.bind("<ButtonRelease-1>", reset_clic) 

#Evenements relatif a la liste de selection
liste.bind("<<ListboxSelect>>", selection)

##Fonction de mise à jour
def update():
    if not(pause) :
        bouge_indiv()
        sortir_indiv()
        
        stat_nbIndiv()
    tk.update_idletasks()
    tk.after(TpsRaffraichissement, update)

##Initialisation
init_case()
init_ligne()
init_texte()
tk.after(TpsRaffraichissement, update)
tk.mainloop()
