from Vect2D import*
import numpy as np
import Variables as Var

class case:
    def __init__(self, pos=vect2D(), dim=0, type=0, score=0, canvas="", color="ivory", explore=False, grille=False) :
        self.pos = pos
        self.dim = dim
        self.type = type # -1 = infranchissable, 0=case normale, 1=sortie, (-2=danger, 2=escalier ?)
        self.score = score
        self.canvas = canvas
        self.color = color
        self.explore = explore
        self.grille = grille
        self.id = canvas.create_rectangle(0,0,dim,dim, fill=color, outline=color)
        self.canvas.move(self.id, pos.x*dim, pos.y*dim)
    
    def raffraichir(self) :
        if(self.type == -1) :
            self.color = "black"
        elif(self.type == 1) :
            self.color = "green"
        elif(self.type == -2) :
            self.color = "red"
        else :
            self.color = "ivory"
        if(self.grille):
            if(self.color == "black") :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "ivory")
            else :
                self.canvas.itemconfig(self.id, fill = self.color, outline = "black")
        else :
            self.canvas.itemconfig(self.id, fill = self.color, outline = self.color)
        return
    
    #Change la couleur en faisant un dégradé entre fg et bg selon score et maxd
    def degrade(self, fg, bg, maxd):
        def blend(i,fg,bg) :
            return (int((1-i)*fg[0]+i*bg[0]), int((1-i)*fg[1]+i*bg[1]), int((1-i)*fg[2]+i*bg[2]))
        col = blend(self.score/maxd, fg, bg)
        if(self.grille) :
            if (col[0] > 255 or col[1] > 255 or col[2] > 255) :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "black")
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "black")
        else :
            if (col[0] > 255 or col[1] > 255 or col[2] > 255) :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % bg, outline = "#%02x%02x%02x" % bg)
            else :
                self.canvas.itemconfig(self.id, fill = "#%02x%02x%02x" % col, outline = "#%02x%02x%02x" % col)
        return
        
        
##Fonction sur le terrain

#Initialisation des cases
def init_case(terrain) :
    Var.TCase = np.array([[case(canvas=terrain)]*Var.largeur]*Var.hauteur,case)
    for x in range(Var.largeur) :
        for y in range(Var.hauteur) :
            pos=vect2D(x,y)
            c = case(pos, Var.dimCase, 0, -1, terrain, "ivory", False)
            Var.TCase[y,x]=c
    return