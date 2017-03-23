sortie = 100
pos = []
Dpos = []
n_individu = 10
vlim = 6
from random import *

def generation_individus():
    while len(pos) < n_individu:
        a = randint(0, sortie - 1)
        if a not in pos:
            pos.append(a)
            Dpos.append(randint(1, vlim))

def tri_individus():
    global pos , Dpos
    L = []
    L2 = []
    for k in range(n_individu):
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
    pos = L
    Dpos = L2

def update():
    global pos, Dpos
    n = len(pos)
    for k in reversed(range(n)):
        pos[k] += Dpos[k]
        if pos[k] > sortie:
            pos.pop(k)
            Dpos.pop(k)
        if k < n_individu - 1 and pos[k] > pos[k+1]:
            pos[k] = pos[k+1] - 1

## Fonctionnement :
generation_individus()
tri_individus()
while len(pos) > 0:
  # affichage
  update()
