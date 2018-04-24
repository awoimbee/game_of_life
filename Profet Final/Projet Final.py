###########################################################################################################
# Maillet William - Arthur Woimbée - JEU DE LA VIE 2D ET 3D                                               #
###########################################################################################################


#Importation de divers modules utiles
import tkinter
import time
import math, _thread
from collections import deque

#######################################
#   FONCTIONS POUR L'AFFICHAGE 3D     #
#######################################


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
    def __init__(self, pos=(0,0,0)):
        #On calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(pos[0]+X, pos[1]+Y, pos[2]+Z) for X,Y,Z in self.vertices]

class Tree:
    """Classe de l'objet arbre
    elle sert juste à montrer la versatilité du code employé"""
    #Sommets du cube quand il est positionné sur l'origine des repères x,y,z puis ses faces
    vertices = ((-0.00544, 0.809443, -0.939428), (0.019167, -3.227034, 0.022684), (0.637348, 0.809443, -0.705472), (0.028745, -3.227034, 0.02617), (0.979368, 1.00352, -0.113076), (0.033842, -3.227034, 0.034997), (0.860586, 1.00352, 0.560572), (0.032072, -3.227034, 0.045035), (0.33658, 0.809443, 1.000265), (0.024263, -3.227034, 0.051587), (-0.353069, 0.872769, 0.994068), (0.01407, -3.227034, 0.051587), (-0.871465, 1.00352, 0.560572), (0.006262, -3.227034, 0.045035), (-0.990247, 1.00352, -0.113076), (0.004492, -3.227034, 0.034997), (-0.653837, 1.066847, -0.711668), (0.009589, -3.227034, 0.02617), (-0.00229, 0.453387, -0.816288), (0.559453, 0.453387, -0.61183), (0.858351, 0.453387, -0.094124), (0.754545, 0.453387, 0.494589), (0.296607, 0.453387, 0.878845), (-0.306797, 0.516713, 0.872648), (-0.759126, 0.453387, 0.494589), (-0.862932, 0.453387, -0.094124), (-0.569643, 0.516713, -0.618026), (0.015024, -2.516458, -0.139296), (0.131209, -2.516458, -0.097008), (0.193029, -2.516458, 0.010068), (0.171559, -2.516458, 0.13183), (0.076845, -2.516458, 0.211305), (-0.052405, -2.453131, 0.205109), (-0.141511, -2.516458, 0.13183), (-0.162981, -2.516458, 0.010068), (-0.106769, -2.453131, -0.103204), (0.242392, -1.745409, -0.230669), (0.365764, -1.745409, -0.016983), (0.322917, -1.745409, 0.226012), (0.133901, -1.745409, 0.384616), (-0.118452, -1.682083, 0.37842), (-0.30186, -1.745409, 0.226012), (-0.344706, -1.745409, -0.016983), (-0.226943, -1.682082, -0.236866), (0.010529, -1.745409, -0.315061), (0.365054, -0.894761, -0.378129), (0.556331, -0.894761, -0.046827), (0.489901, -0.894761, 0.329917), (0.196847, -0.894761, 0.575818), (-0.191317, -0.831434, 0.569622), (-0.478762, -0.894761, 0.329916), (-0.545192, -0.894761, -0.046827), (-0.359524, -0.831434, -0.384325), (0.005569, -0.894761, -0.508971), (0.47439, -0.136519, -0.50957), (0.726197, -0.136518, -0.073428), (0.638746, -0.136519, 0.422534), (0.252955, -0.136519, 0.74625), (-0.256267, -0.073192, 0.740054), (-0.636448, -0.136519, 0.422534), (-0.723899, -0.136518, -0.073428), (-0.477702, -0.073192, -0.515766), (0.001149, -0.136518, -0.681816), (0.015674, -2.466367, -0.253986), (0.199847, -2.466368, -0.186952), (0.292234, -2.403041, -0.023413), (0.263809, -2.466367, 0.175798), (0.11367, -2.466367, 0.30178), (-0.087932, -2.403041, 0.295584), (-0.232462, -2.466367, 0.175798), (-0.266496, -2.466367, -0.017217), (-0.174109, -2.403041, -0.193148), (0.010725, -1.692862, -0.451635), (0.324917, -1.692862, -0.337279), (0.486486, -1.629535, -0.053915), (0.434034, -1.692862, 0.281558), (0.177903, -1.692862, 0.496478), (-0.162062, -1.629536, 0.490282), (-0.412585, -1.692862, 0.281558), (-0.470645, -1.692862, -0.047718), (-0.309076, -1.629535, -0.343475), (0.005286, -0.842699, -0.671042), (0.463775, -0.842699, -0.504165), (0.702124, -0.779372, -0.087815), (0.623007, -0.842699, 0.398883), (0.249243, -0.842699, 0.712509), (-0.244281, -0.779373, 0.706312), (-0.612436, -0.842699, 0.398883), (-0.697161, -0.842699, -0.081619), (-0.458813, -0.779373, -0.510362), (0.000399, -0.078844, -0.831178), (0.564756, -0.078845, -0.625769), (0.859436, -0.015518, -0.11185), (0.760756, -0.078844, 0.485799), (0.300687, -0.078845, 0.871843), (-0.305499, -0.015518, 0.865646), (-0.759959, -0.078845, 0.485799), (-0.864248, -0.078844, -0.105654), (-0.569569, -0.015518, -0.631965), (0.669916, 0.51294, -0.752068), (1.022565, 0.576267, -0.137744), (0.903752, 0.51294, 0.574081), (0.35487, 0.51294, 1.034648), (-0.367254, 0.576267, 1.028452), (-0.910528, 0.51294, 0.574081), (-1.034949, 0.512941, -0.131548), (-0.682301, 0.576267, -0.758265), (-0.003388, 0.512941, -0.997131), (0.747414, 1.054853, -0.845319), (1.143143, 1.118179, -0.156378), (1.009368, 1.054853, 0.6403), (0.394483, 1.054853, 1.15625), (-0.413802, 1.118179, 1.150053), (-1.023078, 1.054853, 0.640299), (-1.162461, 1.054853, -0.150182), (-0.766733, 1.118179, -0.851516), (-0.006855, 1.054853, -1.119851), (-0.018886, 1.895607, -0.373037), (-0.018886, 0.720161, -0.373037), (0.231064, 1.895607, -0.282063), (0.231064, 0.720161, -0.282063), (0.36406, 1.895607, -0.051708), (0.36406, 0.720161, -0.051708), (0.317871, 1.895607, 0.210242), (0.317871, 0.720161, 0.210242), (0.11411, 1.895607, 0.381218), (0.11411, 0.720161, 0.381218), (-0.151881, 1.895607, 0.381218), (-0.151881, 0.720161, 0.381218), (-0.355642, 1.895607, 0.210242), (-0.355642, 0.720161, 0.210242), (-0.401831, 1.895607, -0.051708), (-0.401831, 0.720161, -0.051708), (-0.268836, 1.895607, -0.282063), (-0.268836, 0.720161, -0.282063), (-0.018886, 1.31439, -0.264436), (0.161257, 1.31439, -0.19887), (0.257109, 1.31439, -0.03285), (0.22382, 1.31439, 0.155942), (0.076966, 1.31439, 0.279167), (-0.114738, 1.31439, 0.279166), (-0.261591, 1.31439, 0.155942), (-0.29488, 1.31439, -0.03285), (-0.199028, 1.31439, -0.19887))
    faces = ((63, 1, 3, 64), (64, 3, 5, 65), (65, 5, 7, 66), (66, 7, 9, 67), (67, 9, 11, 68), (68, 11, 13, 69), (69, 13, 15, 70), (3, 1, 17, 15, 13, 11, 9, 7, 5), (71, 17, 1, 63), (70, 15, 17, 71), (0, 2, 4, 6, 8, 10, 12, 14, 16), (114, 25, 26, 115), (115, 26, 18, 116), (113, 24, 25, 114), (112, 23, 24, 113), (111, 22, 23, 112), (110, 21, 22, 111), (109, 20, 21, 110), (108, 19, 20, 109), (116, 18, 19, 108), (79, 34, 35, 80), (80, 35, 27, 72), (78, 33, 34, 79), (77, 32, 33, 78), (76, 31, 32, 77), (75, 30, 31, 76), (74, 29, 30, 75), (73, 28, 29, 74), (72, 27, 28, 73), (81, 44, 36, 82), (82, 36, 37, 83), (83, 37, 38, 84), (84, 38, 39, 85), (85, 39, 40, 86), (86, 40, 41, 87), (87, 41, 42, 88), (89, 43, 44, 81), (88, 42, 43, 89), (97, 51, 52, 98), (98, 52, 53, 90), (96, 50, 51, 97), (95, 49, 50, 96), (94, 48, 49, 95), (93, 47, 48, 94), (92, 46, 47, 93), (91, 45, 46, 92), (90, 53, 45, 91), (107, 62, 54, 99), (99, 54, 55, 100), (100, 55, 56, 101), (101, 56, 57, 102), (102, 57, 58, 103), (103, 58, 59, 104), (104, 59, 60, 105), (106, 61, 62, 107), (105, 60, 61, 106), (34, 70, 71, 35), (35, 71, 63, 27), (33, 69, 70, 34), (32, 68, 69, 33), (31, 67, 68, 32), (30, 66, 67, 31), (29, 65, 66, 30), (28, 64, 65, 29), (27, 63, 64, 28), (44, 72, 73, 36), (36, 73, 74, 37), (37, 74, 75, 38), (38, 75, 76, 39), (39, 76, 77, 40), (40, 77, 78, 41), (41, 78, 79, 42), (43, 80, 72, 44), (42, 79, 80, 43), (51, 88, 89, 52), (52, 89, 81, 53), (50, 87, 88, 51), (49, 86, 87, 50), (48, 85, 86, 49), (47, 84, 85, 48), (46, 83, 84, 47), (45, 82, 83, 46), (53, 81, 82, 45), (62, 90, 91, 54), (54, 91, 92, 55), (55, 92, 93, 56), (56, 93, 94, 57), (57, 94, 95, 58), (58, 95, 96, 59), (59, 96, 97, 60), (61, 98, 90, 62), (60, 97, 98, 61), (25, 105, 106, 26), (26, 106, 107, 18), (24, 104, 105, 25), (23, 103, 104, 24), (22, 102, 103, 23), (21, 101, 102, 22), (20, 100, 101, 21), (19, 99, 100, 20), (18, 107, 99, 19), (0, 116, 108, 2), (2, 108, 109, 4), (4, 109, 110, 6), (6, 110, 111, 8), (8, 111, 112, 10), (10, 112, 113, 12), (12, 113, 114, 14), (16, 115, 116, 0), (14, 114, 115, 16), (135, 118, 120, 136), (136, 120, 122, 137), (137, 122, 124, 138), (138, 124, 126, 139), (139, 126, 128, 140), (140, 128, 130, 141), (141, 130, 132, 142), (120, 118, 134, 132, 130, 128, 126, 124, 122), (143, 134, 118, 135), (142, 132, 134, 143), (117, 119, 121, 123, 125, 127, 129, 131, 133), (131, 142, 143, 133), (133, 143, 135, 117), (129, 141, 142, 131), (127, 140, 141, 129), (125, 139, 140, 127), (123, 138, 139, 125), (121, 137, 138, 123), (119, 136, 137, 121), (117, 135, 136, 119))
    def __init__(self, pos=(0,0,0)):
        #On calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(pos[0]+X, pos[1]+Y, pos[2]+Z) for X,Y,Z in self.vertices]


def keydown(event):
    "Fonction appelée lors de l'apuui d'une touche"
    global pressedkeys
    if event.keysym not in pressedkeys:
        pressedkeys.append(event.keysym)


def keyup(event):
    "Fonction appelée lorsqu'on relache une touche"
    global pressedkeys
    if event.keysym in pressedkeys:
        pressedkeys.pop(pressedkeys.index(event.keysym))


def movement():
    "Calcule le déplacement de la camera"
    global cam, pressedkeys, rendering, keys
    sensMouv = 1/2 #Sensibilite des mouvements
    sensRot = 1/6 #Sensibilite de la rotation
    while(rendering):
        time.sleep(0.03)
        for key in pressedkeys:
            #Déplacement
            sin,cos = math.sin(cam.rot[1])*sensMouv, math.cos(cam.rot[1])*sensMouv
            if key == keys[3]: #aller a droite
                cam.pos[0]+=cos
                cam.pos[2]-=sin
            elif key == keys[1]: #aller a gauche
                cam.pos[0]-=cos
                cam.pos[2]+=sin
            elif key == keys[0]: #on avance
                cam.pos[0]+=sin
                cam.pos[2]+=cos
            elif key == keys[2]: #on recule
                cam.pos[0]-=sin
                cam.pos[2]-=cos
            elif key == keys[4]: #on monte
                cam.pos[1]+=sensMouv
            elif key == keys[5]: #on descent
                cam.pos[1]-=sensMouv
            #Rotation
            # Axe X  |  Axe Y
            # rot[1] |  rot[0]
            elif key == 'Left': #on tourne à gauche
                cam.rot[1]-=sensRot
            elif key == 'Right':
                cam.rot[1]+=sensRot
            elif key == 'Up':
                cam.rot[0]-=sensRot
            elif key == 'Down':
                cam.rot[0]+=sensRot
            else :
                continue


def rotate2D(vertex, rotation):
    "Rotation en 2 dimensions de l'axe partant de l'origine vers le point vertex"
    #https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
    sin=math.sin(rotation)
    cos=math.cos(rotation)
    return vertex[0]*cos-vertex[1]*sin, vertex[1]*cos+vertex[0]*sin


def close():
    "Ferme la fenetre de rendu 3D"
    global rendering
    rendering = False


def changeKb(butt_id):
    "Change la disposition du clavier"
    global keys
    if butt_id == 0:
        keys = ('z','q','s','d','a','e')
    elif butt_id == 1:
        keys = ('w','a','s','d','q','e')

def updateSwitch(start):
    "Démarre ou arrête la mise à jour du rendu 3D et l'algorithme 2D"
    global realTime
    if start == 0:
         realTime = True
    elif start == 1 :
        realTime = False
    else :
        stop() #stoppe l'algorithme 2D


def selectShowOldObjects(nb):
    "Définit le nombre de générations d'objets à afficher"
    global showOldObj
    showOldObj = nb


def window_mainloop():
    "Création de la fenêtre, calcul du rendu 3D"
    from PIL import ImageTk, Image
    import tkinter
    global width3D, height3D, sWidth, sHeight, rendering, objects, showOldObj

    root3D = tkinter.Tk()
    ######## INTERFACE INTERACTIONS UTILISATEUR/PROGRAMME ########
    menubar = tkinter.Menu(root3D)
    root3D.config(menu=menubar)
    
    keybMenu = tkinter.Menu(menubar)
    keybMenu.add_command(label="Français (azerty)", command=lambda : changeKb(0))
    keybMenu.add_command(label="Américain (qwerty)", command=lambda : changeKb(1))

    updateMenu = tkinter.Menu(menubar)
    updateMenu.add_command(label="Affichage 3D en temps réel", command=lambda : updateSwitch(0))
    updateMenu.add_command(label="Ne pas mettre à jour l'affichage 3D", command=lambda : updateSwitch(1))
    updateMenu.add_command(label="Tout mettre en pause", command=lambda : updateSwitch(2))

    oldObjectsMenu = tkinter.Menu(menubar)
    oldObjectsMenu.add_command(label="1", command=lambda : selectShowOldObjects(1))
    oldObjectsMenu.add_command(label="2", command=lambda : selectShowOldObjects(2))
    oldObjectsMenu.add_command(label="3", command=lambda : selectShowOldObjects(3))
    oldObjectsMenu.add_command(label="4", command=lambda : selectShowOldObjects(4))
    oldObjectsMenu.add_command(label="5", command=lambda : selectShowOldObjects(5))
    
    menubar.add_cascade(label="▼Clavier", menu=keybMenu)
    menubar.add_cascade(label="▼Affichage en temps réel", menu=updateMenu)
    menubar.add_cascade(label="▼Nombre de génération d'objets à afficher", menu=oldObjectsMenu)

    #Création du canvas et paramétrage de la récupération de l'entrée utilisateur
    canvas3D = tkinter.Canvas(root3D, width=width3D, height=height3D)
    canvas3D.grid(row=1, columnspan = 5, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
    root3D.bind("<KeyPress>", keydown)
    root3D.bind("<KeyRelease>", keyup)
    root3D.protocol("WM_DELETE_WINDOW", close)

    ##Fond d'ecran
    img = Image.open("./background.jpg")
    x, y = int(height3D*(16/9)), height3D
    img = img.resize((x,y))
    tkimg = ImageTk.PhotoImage(master=root3D, image=img)
    canvas3D.create_image(sWidth, sHeight, image=tkimg) #SWidth et SHeight servent a mettre le milieu de l'image au centre du canvas

    _thread.start_new_thread(movement, ( )) #Les déplacements sont calculés dans un autre thread (=coeur du processeur)

    color = ['white', "grey75", 'grey40', "grey20", "grey1"] #on définit la couleur des cubes en fonction de leur "âge"
    while rendering:
        """ Le rendu 3D est fait ici """
        
        canvas3D.delete("cube") #On remet l'image à 0
        face_list=[] #Contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), int(couleur), int(profondeur) ], [ (x,y),...], ...]
        #On calcule comment dessiner chaque cube
        for gen_nb in range(showOldObj):
            for obj in objects[gen_nb] : #pour chaque objet dans la liste des objets
                obj_faces=[]
                for face in obj.faces: #pour chaque face de l'objet
                    depth = 0
                    face_points = [] #Contient 4 sommets à connecter -> (x,y),(x,y),(x,y),(x,y)
                    for face_vert_id in face:
                        x,y,z = obj.vertices[face_vert_id] #pour chaque point de la face, dont la position est constituée de 3 coordonnées : x,y,z
                        #La caméra est à l'origine des axes. Ce sont les objets qui se déplacent et non la caméra.
                        x-=cam.pos[0]
                        y-=cam.pos[1]+gen_nb
                        z-=cam.pos[2]

                        x,z = rotate2D((x,z), cam.rot[1]) #x et z modifies par la rotation autour de y
                        y,z = rotate2D((y,z), cam.rot[0]) #y et z modifies par la rotation autour de x
                        if z<=0:
                            #On affiche pas ce qui est hors champ
                            face_points = None
                            break
                        f=sWidth/z #Coefficient de stéréoscopie - c'est le FOV
                        #Calcul de la position (en pixels) du sommet sur le canvas ; on ajoute Swidth et Sheight car on veut que (0,0,0) soit placé au milieu du canvas :
                        X,Y = int(x*f)+sWidth, int(y*f)+sHeight 
                        if not -sWidth<X<width3D+sWidth or not -sHeight<Y<height3D+sHeight :
                            #On affiche pas ce qui est hors champ
                            face_points = None
                            break
                        face_points.append((X, Y)) #Position en pixels des sommets sur l'image 2D
                        depth += (x**2)+(y**2)+(z**2) #On ajoute la distance point-caméra à la "distance" totale de la face
                    if not face_points:
                        #On arrête de calculer les faces de l'objet si une d'entre elles n'est pas à l'écran
                        break
                    face_points.append(depth) #on ajoute à face_points les coordonnées des points de la face et la "distance totale" de la face
                    obj_faces.append(face_points) #On ajoute la face à la liste des faces de l'objet
                if not obj_faces :
                    #si aucune face de l'objet n'est affichée
                    continue
                #On trie les faces des objets selon leur "distance" ou "profondeur" (de la plus grande à la plus petite)
                obj_faces.sort(key=lambda x: x[-1], reverse=True)
                #On ajoute les faces de l'objet à la liste de toutes les faces en ne gardant que les trois faces les plus proches et la couleur de l'objet, les trois autres n'étant pas visibles 
                obj_faces.append(color[gen_nb])
                face_list.append(obj_faces[-4:])
        #On trie les objets selon la "distance" d'une de ses faces choisie arbitrairement (de la plus grande à la plus petite)
        face_list.sort(key=lambda x: x[0][-1], reverse=True)
        #On dessine les objets/faces :
        for obj_faces in face_list:
            col=obj_faces.pop()
            for face in obj_faces :
                canvas3D.create_polygon(face[:-1], fill=col, outline="black", tag="cube")
        root3D.update()
    #fin du "While"
    root3D.destroy() #on ferme la fenêtre
    return


def newLine3D(board) :
    "Accepte un plateau de jeu 2D, le transforme en objets 3D"
    global realTime, objects
    #self.objects = [ Cube((X,0,Y), board[Y][X], True) if X!=0 and Y!=0 and X!=len(board[0])-1 and Y!=len(board)-1 else Cube((X,0,Y), board[Y][X])   for X in range(len(board[0])) for Y in range(len(board)) ]
    if realTime :
        objects.appendleft([ Cube((X,0,Y)) for X in range(len(board[0])) for Y in range(len(board)) if board[Y][X] ])
        objects.pop()


def launch3DWindow():
    "Lance la fenêtre du jeu de la vie en 3D"
    global rendering
    rendering=True
    _thread.start_new_thread(window_mainloop, ( )) #on attend pas la fin de l'exécution de window_mainloop


def initialise(in_height, in_width):
    "Met en place certaines variables necessaires au rendu 3D, vestige d'anciennes implémentations"
    global height3D, width3D, cam, sWidth, sHeight
    height3D = in_height
    width3D = in_width
    sWidth, sHeight = int(width3D/2), int(height3D/2)


pressedkeys = []
objects = deque([[],[],[],[],[]])
showOldObj = 1
rendering=False
keys = ('w','a','s','d','q','e')
realTime=True
height3D, width3D = 500, 600
sHeight, sWidth = 250, 300
cam = Camera()




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

                # #Parcours des voisins dans un rayon de 1, soit 3x3 cases
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        #Ajout de la valeur de la case à "neighbors"
                        neighbors+=board[(row+i+boardHeight)%boardHeight][(column+j+boardWidth)%boardWidth]
                #neighbors=sum([board[row+i][column+j] for j in range(-1,2) for i in range(-1,2) if column+j<boardWidth and row+i<boardHeight])

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
        newLine3D(board)

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
    newLine3D(board)
    display()

def clearAll():
    "Efface toute les cellules"
    global board, step

    #Ré-initialisation des étapes
    step = 0
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Affichage
    display()


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


def clock():
    "Trace un vaisseau spatial dans le jeu de la vie"
    global board

    #Centre du vaisseau, au centre du canvas
    middleX = boardWidth//2
    middleY = boardHeight//2
    #Remise à 0 du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Ouverture d'un fichier qui contient des coordonnées
    f = open("clock.txt", "r")
    clockY, clockX = [], []
    #Ajout de chaques coordonnées dans une liste
    for l in f:
        row = l.split() #Transformation d'un caractère en liste
        clockY.append(row[0]) #Ajout de la première coordonnée
        clockX.append(row[1]) #De la deuxième

    #Traçage du vaisseau dans le canvas
    for i in range(len(clockY)):
        board[middleY+int(clockY[i])][middleX+int(clockX[i])] = 1

    display()
   
##########################################
#          PROGRAMME PRINCIPAL           #
##########################################

if __name__ == "__main__":

    ######## INITIALISATION DES VARIABLES ########
    #Taille d'une case en pixels
    caseSize = 10
    #Largeur du tableau
    boardWidth = 90
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
    initialise(700,900)


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
    tkinter.Button(userPart, text="Visualisation en 3D", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=launch3DWindow).grid(row=1, column=2, padx=5, pady=5)

    ######## BOUTONS POUR DIVERSES FORMES ########
    tkinter.Button(userPart, text="Vaisseau", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=ship).grid(row=2, column=2, padx=5, pady=5)
    tkinter.Button(userPart, text="Horloge", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=clock).grid(row=3, column=2, padx=5, pady=5)
    

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
