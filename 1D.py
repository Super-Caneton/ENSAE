sortie = 100  #Les individus sont placés sur des cases de 0 à sortie (sortie non incluse)
from random import *

def generation_individus(n, v):
    '''génère n individu à des positions aléatoire avec des vitesses aléatoires inférieure à v'''
    pos = []
    Dpos = []
    while len(pos) < n:
        a = randint(0, sortie - 1)
        if a not in pos:
            pos.append(a)
            Dpos.append(randint(1, v))
    return (pos, Dpos)

def tri_individus(pos, Dpos):
    '''algorithme de tri des position avec déplacement des vitesses correspondantes'''
    L = []
    L2 = []
    n = len(pos)
    for k in range(n):
        l = len(L)
        i = 0 
        while i < l and L[i] < pos[k]:
           i += 1
        if i == l :
            L.append(pos[k])
            L2.append(Dpos[k])
        else:
            L = L[:i] + [pos[k]] + L[i:]
            L2 = L2[:i] + [Dpos[k]] + L2[i:]
    return (L, L2)

def update(pos, Dpos):
    '''calcule le mouvement à l'étape n+1 de chaque individu en fonction de sa vitesse'''
    n = len(pos)
    for k in reversed(range(n)):
        pos[k] += Dpos[k]
        if pos[k] > sortie:
            pos.pop(k)
        if k < len(pos) - 1 and pos[k] >= pos[k+1]:
            pos[k] = pos[k+1] - 1
    return (pos, Dpos)

import matplotlib.pyplot as plt
import numpy as np

def temps_de_sortie_embouteillage(n, v):
    '''affiche le temps de sortie (nombre d'étapes) nécessaire pour évacuer tous les individus'''
    (pos,Dpos) = generation_individus(n, v)
    (pos,Dpos) = tri_individus(pos, Dpos)
    compteur = 0
    embouteillage_max = 0
    while len(pos) > 0:
        for k in range(len(pos)):
            for i in range(1, len(pos) - k):
                if pos[k+i] == pos[k] + i and embouteillage_max < i:
                    embouteillage_max = i
        (pos, Dpos) = update(pos, Dpos)
        compteur += 1
    return (compteur, embouteillage_max)

def fonction_temps_de_sortie(n_max):
    ''' permet de connaitre le temps de sortie en fonction de n'''
    nb_etapes = []
    for k in range(1, n_max):
        m = 0
        for i in range(40):
            (temps, _) = temps_de_sortie_embouteillage(k, 10)
            m += temps
        m /= 40
        nb_etapes.append(m)
    return nb_etapes

def trace_etape(nb_etapes):
    '''permet d'afficher une liste dans un plot (utile pour trouver un modèle avant le fittage R)'''
    n = len(nb_etapes)
    plt.scatter([k/sortie for k in range(1, n + 1)],nb_etapes)
    plt.show()
    
def fonction_taille_embouteillage(n_max):
    ''' affiche la taille de l'embouteillage maximal (suite consécutive de personne qui sont bloquées parce que le premier ne va pas assez vite) en fonction de n'''
    nb_etapes = []
    for k in range(1, n_max):
        m = 0
        for i in range(60):
            (_, maxi) = temps_de_sortie_embouteillage(k, 10)
            m += maxi
        m /= 60
        nb_etapes.append(m)
    return nb_etapes

def fonction_temps_de_sortie2(v_max):
    '''fonction du nombre d'étape en fonction de la vitesse maximale'''
    nb_etapes = []
    for k in range(1, v_max):
        m = 0
        for i in range(60):
            (temps, _) = temps_de_sortie_embouteillage(60, k)
            m += temps
        m /= 60
        nb_etapes.append(m)
    return nb_etapes
           
def fonction_taille_embouteillage2(v_max):
    '''fonction de la taille de la congestion en fonction de la vitesse maximale'''
    nb_etapes = []
    for k in range(1, v_max):
        m = 0
        for i in range(60):
            (_, maxi) = temps_de_sortie_embouteillage(40, k)
            m += maxi
        m /= 60
        nb_etapes.append(m)
    return nb_etapes
# generation_individus()
# tri_individus()
# compteur = 0
# while len(pos) > 0:
#     plt.scatter(pos, [compteur for k in range(len(pos))])
#     update()
#     compteur += 1
# plt.show()
# print(compteur)
        
            
