###########################################################################################################
# Maillet William - Arthur Woimbée - JEU DE LA VIE 2D ET 3D                                               #
###########################################################################################################


#Importation de divers modules utiles
import tkinter
import time
from PIL import ImageTk, Image
import math
import _thread

##########################################
#               CLASSES                  #
##########################################
class Camera:
    "Classe de la caméra"
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos) #pos = x,y,z
        self.rot = list(rot) #rot=rotation

class Cube:
    "Classe de l'objet cube"
    #Sommets du cube quand il est positionné sur l'origine des repères x,y,z puis ses faces
    vertices = (-0.5,0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5), (-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5)
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
    life = int()
    def __init__(self, pos=(0,0,0)):
        #On calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(pos[0]+X, pos[1]+Y, pos[2]+Z) for X,Y,Z in self.vertices]

class RenderingIn3D :
    "Classe principale du moteur 3D"
    def keydown(self, event):
        if event.keysym not in self.pressedkeys:
            self.pressedkeys.append(event.keysym)
    def keyup(self, event):
        if event.keysym in self.pressedkeys:
            self.pressedkeys.pop(self.pressedkeys.index(event.keysym))

    def movement(self):
        "Calcule le déplacement de la camera"
        sensMouv = 1/2 #Sensibilite des mouvements
        sensRot = 1/6 #Sensibilite de la rotation
        while(self.rendering):
            time.sleep(0.03)
            for key in self.pressedkeys:
                #Déplacement
                sin,cos = math.sin(self.cam.rot[1])*sensMouv, math.cos(self.cam.rot[1])*sensMouv
                if key == 'd':
                    self.cam.pos[0]+=cos
                    self.cam.pos[2]-=sin
                elif key == 'a':
                    self.cam.pos[0]-=cos
                    self.cam.pos[2]+=sin
                elif key == 'w': #on avance
                    self.cam.pos[0]+=sin
                    self.cam.pos[2]+=cos
                elif key == 's': #on recule
                    self.cam.pos[0]-=sin
                    self.cam.pos[2]-=cos
                elif key == 'q':
                    self.cam.pos[1]+=sensMouv
                elif key == 'e':
                    self.cam.pos[1]-=sensMouv
                #Rotation
                # Axe X  |  Axe Y
                # rot[1] |  rot[0]
                elif key == 'Left': #on tourne à gauche
                    self.cam.rot[1]-=sensRot
                elif key == 'Right':
                    self.cam.rot[1]+=sensRot
                elif key == 'Up':
                    self.cam.rot[0]-=sensRot
                elif key == 'Down':
                    self.cam.rot[0]+=sensRot
                # elif key == 'Escape':
                #     _thread.interrupt_main() #exit

    def rotate2D(self, vertex, rotation):
        "Rotation en 2 dimensions de l'axe partant de l'origine vers le point vertex"
        #https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
        sin=math.sin(rotation)
        cos=math.cos(rotation)
        return vertex[0]*cos-vertex[1]*sin, vertex[1]*cos+vertex[0]*sin

    def close(self):
        self.rendering = False

    def window_mainloop(self):
        "Création de la fenêtre"
        root3D = tkinter.Tk()
        frame = tkinter.Frame(root3D, width=self.width, height=self.height)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        #Création du canvas et paramétrage de la récupération de l'entrée utilisateur
        canvas = tkinter.Canvas(frame, width=self.width, height=self.height, bg="#bbbbbb")
        canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        root3D.bind("<KeyPress>", self.keydown)
        root3D.bind("<KeyRelease>", self.keyup)
        root3D.protocol("WM_DELETE_WINDOW", self.close)
        frame.pack()

        _thread.start_new_thread(self.movement, ( )) #Les déplacements sont calculés dans un autre thread (=coeur du processeur)
        while self.rendering:
            """ Le rendu 3D est fait ici """
            canvas.delete("all") #On remet l'image à 0
            face_list=[] #Contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), int(couleur), int(profondeur) ], [ (x,y),...], ...]
            #On calcule comment dessiner chaque cube
            for obj in self.objects :
                obj_faces=[]
                for face in obj.faces:
                    depth = 0
                    face_points = [] #Contient 4 sommets à connecter -> (x,y),(x,y),(x,y),(x,y)
                    for x,y,z in (obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]], obj.vertices[face[3]]):
                        #La caméra est à l'origine des axes. Ce sont les objets qui se déplacent et non la caméra.
                        x-=self.cam.pos[0]
                        y-=self.cam.pos[1]
                        z-=self.cam.pos[2]

                        x,z = self.rotate2D((x,z),self.cam.rot[1]) #x et z modifies par la rotation autour de y
                        y,z = self.rotate2D((y,z),self.cam.rot[0]) #y et z modifies par la rotation autour de x
                        if z<=0:
                            #On affiche pas ce qui est hors champ
                            face_points = None
                            break
                        f=self.sWidth/z #Coefficient de stéréoscopie
                        X,Y = int(x*f)+self.sWidth, int(y*f)+self.sHeight #Position en pixels des sommets sur l'image 2D ; +Swidth et +Sheight car le repere xyz est placé au milieu de l'ecran
                        if not -self.sWidth<X<self.width+self.sWidth or not -self.sHeight<Y<self.height+self.sHeight :
                            #On affiche pas ce qui est hors champ
                            face_points = None
                            break
                        face_points.append((X, Y)) #Position en pixels des sommets sur l'image 2D
                        depth += (x**2)+(y**2)+(z**2) #Se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D
                    if not face_points:
                        #On arrête de calculer les faces de l'objet
                        break
                    face_points.append(depth) #face_points contient les coordonnées des points de la face, mais aussi la profondeur de la face
                    obj_faces.append(face_points)
                if not obj_faces :
                    continue
                #On trie les faces des objets et les ajoute à la liste de toutes les faces
                obj_faces.sort(key=lambda x: x[-1], reverse=True)
                face_list.append(obj_faces) #[-3:] Car on ne dessine que les 3 faces maximum visibles simultanément de chaque cube
            #On trie les objets
            face_list.sort(key=lambda x: x[0][-1], reverse=True)
            #On dessine les objets/faces :
            for obj_faces in face_list:
                for face in obj_faces :
                    canvas.create_polygon(face[:-1], fill="#000000", outline="white")
            root3D.update()
        root3D.destroy()

    def newLine(self, board) :
        #self.objects = [ Cube((X,0,Y), board[Y][X], True) if X!=0 and Y!=0 and X!=len(board[0])-1 and Y!=len(board)-1 else Cube((X,0,Y), board[Y][X])   for X in range(len(board[0])) for Y in range(len(board)) ]
        if self.rendering :
            self.objects = [ Cube((X,0,Y)) for X in range(len(board[0])) for Y in range(len(board)) if board[Y][X] ]

    def launchWindow(self):
        "Lance la fenêtre du jeu de la vie en 3D"
        self.rendering=True
        _thread.start_new_thread(self.window_mainloop, ( )) #on attend pas la fin de l'exécution de window_mainloop

    def __init__(self, cam, height, width):
        self.pressedkeys = []
        self.objects = []
        self.height = height
        self.width = width
        self.cam = cam
        self.sWidth, self.sHeight = int(width/2), int(height/2)
        self.rendering=False


##########################################
#   FONCTIONS DU JEU DE LA VIE EN 2D     #
##########################################

def display():
    "Affiche un tableau dans le canvas à partir de la liste"
    global board

    #Effacer toute les cellules
    canvas.delete("cell")

    #Coordonnées dans le canvas qui servent à placer les carrés
    x, y = 0, 0
    #Parcours du tableau de long en large
    for row in range(len(board)):
        for column in range(len(board[0])):

            #On trace seulement si la case est vivante
            if board[row][column] == 1:
                canvas.create_rectangle(x, y, x+caseSize, y+caseSize, fill="black", tag="cell", outline="grey")

            #On passe a la cellule suivante
            x += caseSize

            #Retour à la ligne
            if x >= boardWidth*caseSize:
                x = 0

        y += caseSize

    #Affichage final
    time.sleep(0.02)
    root.update()

def neighborsFinding():
    "Chercher voisins + calculer couleur nouvelle case"
    global keepgoing, step, board, boardWidth, boardHeight

    #Démarrage du processus
    keepgoing = True

    #Calcul des voisins
    while keepgoing:

        #Copie intégrale du tableau
        board_new=[[0 for i in range(boardWidth)] for j in range(boardHeight)]

        #Parcours du tableau de long en large
        for row in range(len(board)):
            for column in range(len(board[0])):

                #Voisins initialisés à 0
                neighbors = 0

                #Parcours des voisins dans un rayon de 1, soit 3x3 cases
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        #Ajout de la valeur de la case à "neighbors"
                        neighbors+=board[(row+i+boardHeight)%boardHeight][(column+j+boardWidth)%boardWidth]

                #Retrait de la cellule étudiée (pas voisine)
                neighbors -= board[row][column]

                #Application des règles du jeu de la vie
                if board[row][column]==1 and (neighbors<2 or neighbors >3):
                    board_new[row][column] = 0    #Mort car pas assez de cellules voisines

                elif board[row][column]==1 and (neighbors==2 or neighbors==3):
                    board_new[row][column] = 1    #Vie qui continue

                elif board[row][column]==0 and neighbors==3:
                    board_new[row][column] = 1    #Naissance car 3 cellules voisines

                else:
                    board_new[row][column] = board[row][column]

        #Mise à jour de l'ancien tableau
        board=board_new

        #Actualisation du tableau de la partie 3D
        renderer3D.newLine(board)

        #Mise à jour de l'étape et de l'état
        step += 1
        state.set("En cours" + " (étape "+ str(step) + ")")

        #Affichage
        display()

def stop():
    "Arrête le programme grâce à un interrupteur"
    global keepgoing, step

    #On arrête le processus de calcul des voisins
    keepgoing = False
    state.set("Arrêtée" + " (étape "+ str(step) + ")")

def changeColor(event):
    "Change la couleur de la case cliquée"

    #Affichage des coordonnées dans le canvas
    canvCoords.set("Coordonnées : " + str(event.x) + " ; " + str(event.y))

    #Calcul et affichage des coordonnées dans la case dans le tableau
    boardColumn = event.x//caseSize
    boardRow = event.y//caseSize
    boardCoords.set("Dans le tableau : " + str(boardColumn) + " ; " + str(boardRow))

    #Si on clique sur une case blanche, elle devient noire
    if board[boardRow][boardColumn]==0:
        board[boardRow][boardColumn] = 1

    #Si on clique sur une case noire, elle devient blanche
    elif board[boardRow][boardColumn]==1:
        board[boardRow][boardColumn] = 0

    #Affichage
    renderer3D.newLine(board)
    display()

def clearAll():
    "Efface toute les cellules"
    global board, step

    #Ré-initialisation des étapes
    step = 0
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Affichage
    display()

def launch3D():
    "Lance le jeu de la vie en 3D"
    renderer3D.launchWindow()

def ship():
    "Trace un vaisseau spatial dans le jeu de la vie"
    global board

    #Centre du vaisseau, au centre du canvas
    middleX = boardWidth//2
    middleY = boardHeight//2
    #Remise à 0 du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Ouverture d'un fichier qui contient des coordonnées
    f = open("ship.txt", "r")
    shipY, shipX = [], []
    #Ajout de chaques coordonnées dans une liste
    for l in f:
        row = l.split() #Transformation d'un caractère en liste
        shipY.append(row[0]) #Ajout de la première coordonnée
        shipX.append(row[1]) #De la deuxième

    #Traçage du vaisseau dans le canvas
    for i in range(len(shipY)):
        board[middleY+int(shipY[i])][middleX+int(shipX[i])] = 1

    display()

##########################################
#          PROGRAMME PRINCIPAL           #
##########################################

if __name__ == "__main__":

    ######## INITIALISATION DES VARIABLES ########
    #Taille d'une case en pixels
    caseSize = 20
    #Largeur du tableau
    boardWidth = 40
    #Hauteur du tableau
    boardHeight = 30
    #Interrupteur
    keepgoing=True
    #Étapes
    step = 0
    #Initialisation de la fenêtre
    root = tkinter.Tk()
    root.title("Le Jeu de La Vie")
    #Fond de la fenêtre
    root.configure(background="grey")
    #Initialisation du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]
    #Initialisation du jeu de la vie en 3D
    renderer3D = RenderingIn3D(Camera((0,0,-5)), 700, 900)



    ######## TABlEAU ########
    canvas = tkinter.Canvas(root, width=caseSize*boardWidth, height=caseSize*boardHeight, bg="white", bd=0, highlightthickness=0)
    canvas.grid(column=1, row=1, padx=2, pady=2, columnspan=100)
    canvas.bind("<Button-1>", changeColor) #Localisation des clics dans le canvas3
    canvas.bind("<B1-Motion>", changeColor)


    ######## INTERFACE INTERACTIONS UTILISATEUR/PROGRAMME ########
    userPart = tkinter.LabelFrame(root, bd=2, text="Utilisateur", bg="grey", fg="white", font=("Calibri", 12))
    userPart.grid(column=100, row=2, padx=5, pady=2, sticky=tkinter.W)

    #Bouton de lancement
    launchButton = tkinter.Button(userPart, text="Lancer la simulation", command=neighborsFinding, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    launchButton.grid(column=1, row=1, padx=7, pady=5)
    #Bouton de stop
    stopButton = tkinter.Button(userPart, text="Stopper la simulation", command=stop, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    stopButton.grid(column=1, row=2, padx=7, pady=5)
    #Bouton de clear
    clearButton = tkinter.Button(userPart, text="Effacer tout", command=clearAll, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    clearButton.grid(column=1, row=3, padx=7, pady=5)



    ######## INTERFACE INFORMATION ########
    devPart = tkinter.LabelFrame(root, bd=2, text="Informations", bg="grey", fg="white", font=("Calibri", 12))
    devPart.grid(column=99, row=2, padx=5, pady=2, sticky=tkinter.W)

    #Coordonnées dans le canvas
    canvCoords = tkinter.StringVar()
    canvCoords.set("Coordonnées :")
    cDisp1 = tkinter.Label(devPart, textvariable=canvCoords, bg="grey", fg="white", font=("Calibri", 12))
    cDisp1.grid(column=1, row=1, padx=7, pady=5)
    #Coordonnées dans le tableau
    boardCoords = tkinter.StringVar()
    boardCoords.set("Dans le tableau :")
    cDisp2 = tkinter.Label(devPart, textvariable=boardCoords, bg="grey", fg="white", font=("Calibri", 12))
    cDisp2.grid(column=1, row=2, padx=7, pady=5)



    ######## ÉTAT DE LA SIMULATION ########
    statePart = tkinter.LabelFrame(devPart, bd=2, text="État de la simulation", bg="grey", fg="white", font=("Calibri", 12))
    statePart.grid(column=1, row=3, padx=5, pady=5, sticky=tkinter.W)

    state = tkinter.StringVar()
    state.set("Arrêteée")
    stateDisplay = tkinter.Label(statePart, textvariable=state, bg="grey", fg="white", font=("Calibri", 12))
    stateDisplay.grid(column=1, row=1, padx=7, pady=5)

    ######## BOUTON DE LA SIMULATION 3D ########
    tkinter.Button(userPart, text="Visualisation en 3D", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=launch3D).grid(row=1, column=2, padx=5, pady=5)

    ######## BOUTONS POUR DIVERSES FORMES ########
    tkinter.Button(userPart, text="Vaisseau", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=ship).grid(row=2, column=2, padx=5, pady=5)

    #Fenêtre non-redimensionnable
    root.resizable(False, False)

    ######## TRACAGE DU QUADRILLAGE ########
    #Traçage du quadrillage vertical
    a,b = 0,0
    for i in range(len(board)):
        for j in range(len(board[0])):
            canvas.create_line(a, b, a, b+boardHeight*caseSize, fill="grey")
            a += caseSize
    #Traçage d'un quadrillage horizontal
    a, b = 0,0
    for i in range(len(board)):
        for j in range(len(board[0])):
            canvas.create_line(a, b, a+boardWidth*caseSize, b, fill="grey")
            b += caseSize



    #Activation du gestionnaire d'évènement de la fenêtre
    display()
    root.mainloop()
