import numpy as np

from Vect2D import*

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

#False : Voisin de Von Neumann => Croix
#True : Voisin de Moore => Carré
typePinceau = False

pause = False #Met en pause le mouvement des individus
grilleTerrain = False
mode = 1

nvCase = True #Détermine si on a selectionné une nouvelle case
typeCase = 0

#Variables concernant les cases
TCase = np.array([]) #Pour demander la case à la xième colonne, yième ligne écrire TCase[y,x]
dimCase = 20 #Taille de la case en pixels

#Variables concernant les sorties 
LSortie = [] #objets de la forme [x,y]

Tdirection = np.array([[vect2D()]*largeur]*hauteur,vect2D)  #Tableau des vecteur direction
Tligne = np.array([])

Ttexte = np.array([])

#Variables concernant les individus
LIndiv=[]
NIndiv=100
rIndiv=5
vminIndiv=0.5
vmaxIndiv=2

#Statistique
dMaxCase=-1 #Distance maximale d'une case d'une sortie