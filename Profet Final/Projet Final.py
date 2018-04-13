###########################################################################################################
# Maillet William - Test du jeu de la vie                                                                 #
###########################################################################################################


#Importation de divers modules utiles
import tkinter
from random import randint
import time
from PIL import ImageTk, Image
import math, random
import _thread

##########################################
#               CLASSES                  #
##########################################
class Camera:
    "Classe de la caméra"
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

class Cube:
    "Classe de l'objet cube"
    #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses faces
    vertices = (-0.5,0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5), (-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5)
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
    life = int()    
    def __init__(self, pos=(0,0,0), life=0):
        #on calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(pos[0]+X, pos[1]+Y, pos[2]+Z) for X,Y,Z in self.vertices]
        self.life=life

class RenderingIn3D :
    "Classe principale du moteur 3D"
    def keydown(self, event):
        if event.keysym not in self.pressedkeys:
            self.pressedkeys.append(event.keysym)
    def keyup(self, event):
        if event.keysym in self.pressedkeys:
            self.pressedkeys.pop(self.pressedkeys.index(event.keysym))

    def movement(self):
        """Calcule le déplacement de la camera"""
        sensMouv = 1/10 #sensibilite des mouvements
        sensRot = 1/30 #sensibilite de la rotation
        
        while(True):
            time.sleep(0.01)
            for key in self.pressedkeys:
                #déplacement
                x,y = math.sin(self.cam.rot[1])*sensMouv, math.cos(self.cam.rot[1])*sensMouv
                if key == 'd':
                    self.cam.pos[0]+=y
                    self.cam.pos[2]-=x
                elif key == 'a':
                    self.cam.pos[0]-=y
                    self.cam.pos[2]+=x
                elif key == 'w':
                    self.cam.pos[0]+=x
                    self.cam.pos[2]+=y
                elif key == 's':
                    self.cam.pos[0]-=x
                    self.cam.pos[2]-=y

                elif key == 'q':
                    self.cam.pos[1]+=sensMouv
                elif key == 'e':
                    self.cam.pos[1]-=sensMouv

                #rotation
                # axe X  |  axe Y
                # rot[1] |  rot[0]
                elif key == 'Left':
                    self.cam.rot[1]-=sensRot
                elif key == 'Right':
                    self.cam.rot[1]+=sensRot
                elif key == 'Up':
                    self.cam.rot[0]-=sensRot
                elif key == 'Down':
                    self.cam.rot[0]+=sensRot

                elif key == 'Escape':
                    _thread.interrupt_main() #exit

    def rotate2D(self, vertex, rotation):
        """Rotation en 2 dimensions de l'axe partant de l'origine vers le point "vertex" """
        #https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
        sin=math.sin(rotation)
        cos=math.cos(rotation)
        return vertex[0]*cos-vertex[1]*sin, vertex[1]*cos+vertex[0]*sin


    def window_mainloop(self):
        root = tkinter.Tk()
        frame = tkinter.Frame(root, width=self.width, height=self.height)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        #création du canvas et paramétrage de la récupération de l'entrée utilisateur
        canvas = tkinter.Canvas(frame, width=self.width, height=self.height, bg="#343D46")
        canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
        root.bind("<KeyPress>", self.keydown)
        root.bind("<KeyRelease>", self.keyup)
        frame.pack()

    
        i,frameRate=0,0
        while True:
            """ Le rendu 3D est fait ici """
            canvas.delete("all") #on remet l'image à 0
            face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), int(couleur), int(profondeur) ], [ (x,y),...], ...]
            #on calcule comment dessiner chaque cube
            for board in self.objects:
                for obj in board :
                    obj_faces=[]
                    for face in obj.faces:
                        depth = 0
                        face_points = [] #contient 4 sommets a connecter -> (x,y),(x,y),(x,y),(x,y)
                        for x,y,z in (obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]], obj.vertices[face[3]]):
                            #le monde bouge par rapport a la camera
                            x-=self.cam.pos[0]
                            y-=self.cam.pos[1]
                            z-=self.cam.pos[2]

                            x,z = self.rotate2D((x,z),self.cam.rot[1]) #x et z modifies par la rotation autour de y
                            y,z = self.rotate2D((y,z),self.cam.rot[0]) #y et z modifies par la rotation autour de x
                            if z<=0:
                                #on affiche pas ce qui est hors champ
                                face_points = None
                                break
                            f=(self.width/2)/z #coefficient de stereoscopie
                            X,Y = int(x*f)+self.sWidth, int(y*f)+self.sHeight #position en pixels des sommets sur l'image 2D ; +Swidth et +Sheight car le repere xyz est placé au milieu de l'ecran
                            if not 0<X<self.width or not 0<Y<self.height :
                                #on affiche pas ce qui est hors champ
                                face_points = None
                                break
                            face_points.append((X, Y)) #position en pixels des sommets sur l'image 2D
                            depth += (x**2)+(y**2)+(z**2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D
                        if not face_points:
                            #on arrete de calculer les faces de l'objet
                            break
                        face_points.extend( (obj.life, depth) ) #face_points contient les coordonnees des points de la face, mais aussi la couleur et profondeur de la face
                        obj_faces.append(face_points)
                    if not obj_faces :
                        continue
                    #on trie les faces des objets et les ajoutes a la liste de toutes les faces
                    obj_faces.sort(key=lambda x: x[-1], reverse=True)
                    face_list.append(obj_faces[-3:]) #[-3:] car on ne dessine que les 3 faces maximum visibles simultanément de chaque cube
                #on trie les objets
                face_list.sort(key=lambda x: x[0][-1], reverse=True)
                #On dessine les objets/faces :
                for obj_faces in face_list:
                    for face in obj_faces :
                        color = '#000000' if face[-2]==True else "#ffffff" 
                        canvas.create_polygon(face[:-2], fill=color, outline="black")
            root.update()

    def newLine(self, board) :
        if len(self.objects) > 0:
            del self.objects[0]
        self.maxZ += 4
        Z = self.maxZ
        self.objects.append( [ Cube((X,Z,Y), board[Y][X]) for X in range(len(board[0])) for Y in range(len(board)) ] )
        self.cam.pos[1] += 4


    def launchWindow(self):
        "Lance la fenêtre du jeu de la vie en 3D"
        _thread.start_new_thread(self.movement, ( )) #les déplacements sont calculés dans un autre thread
        _thread.start_new_thread(self.window_mainloop, ( ))

        
    def __init__(self, cam, height, width):
        self.pressedkeys = []
        self.objects = []
        self.height = height
        self.width = width
        self.cam = cam
        self.sWidth, self.sHeight = int(width/2), int(height/2)
        self.maxZ = 0
       





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
    time.sleep(0.01)
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
    
    


##########################################
#          PROGRAMME PRINCIPAL           #
##########################################

if __name__ == "__main__":

    ######## INITIALISATION DES VARIABLES ########
    #Taille d'une case en pixels
    caseSize = 20
    #Largeur du tableau
    boardWidth = 20
    #Hauteur du tableau
    boardHeight = 20
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
    canvas.bind("<Button-1>", changeColor) #Localisation des clics dans le canvas


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



    ######## INTERFACE DÉVELOPPEMENT ########
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



    tkinter.Button(root, text="3D", bg="grey", fg="white", command=launch3D).grid(row=2, column=98, padx=5, pady=5)
    
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
