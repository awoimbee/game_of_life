####################################################################
#   MODULE QUI CONTIENT TOUT CE QU'IL FAUT POUR L'AFFICHAGE 3D     #
####################################################################
import math, time, _thread

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


def keydown(event):
    global pressedkeys
    if event.keysym not in pressedkeys:
        pressedkeys.append(event.keysym)


def keyup(event):
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
    global rendering
    rendering = False


def buttCenter(butt_id):
    global keys, realTime
    if butt_id == 0:
        keys = ('z','q','s','d','a','e')
    elif butt_id == 1:
        keys = ('w','a','s','d','q','e')
    elif butt_id == 2:
        realTime = True
    elif butt_id == 3:
        realTime = False


def window_mainloop():
    "Création de la fenêtre"
    from PIL import ImageTk, Image
    import tkinter
    global width, height, sWidth, sHeight, rendering, objects

    root3D = tkinter.Tk()
    ######## INTERFACE INTERACTIONS UTILISATEUR/PROGRAMME ########
    toolbar = tkinter.Frame(root3D, width=width, height=25)
    toolbar.grid(column=0, row=0)
    azertyButtn = tkinter.Button(toolbar, text="azerty", command=lambda : buttCenter(0), bg="#545556", fg="white", relief="flat", font=("Calibri", 10))
    azertyButtn.grid(column=0, row=0)
    qwertyButtn = tkinter.Button(toolbar, text="qwerty", command=lambda : buttCenter(1), bg="#545556", fg="white", relief="flat", font=("Calibri", 10))
    qwertyButtn.grid(column=1, row=0)
    startRealTime = tkinter.Button(toolbar, text="start", command=lambda : buttCenter(2), bg="#545556", fg="white", relief="flat", font=("Calibri", 10))
    startRealTime.grid(column=2, row=0)
    stopRealTime = tkinter.Button(toolbar, text="stop", command=lambda : buttCenter(3), bg="#545556", fg="white", relief="flat", font=("Calibri", 10))
    stopRealTime.grid(column=3, row=0)

    #Création du canvas et paramétrage de la récupération de l'entrée utilisateur
    canvas3D = tkinter.Canvas(root3D, width=width, height=height)
    canvas3D.grid(row=1, columnspan = 5, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
    root3D.bind("<KeyPress>", keydown)
    root3D.bind("<KeyRelease>", keyup)
    root3D.protocol("WM_DELETE_WINDOW", close)
    ##Fond d'ecran
    img = Image.open("./background.jpg")
    x, y = int(height*(16/9)), height
    img = img.resize((x,y))
    tkimg = ImageTk.PhotoImage(master=root3D, image=img)
    canvas3D.create_image(sWidth, sHeight, image=tkimg) #SWidth et SHeight servent a mettre le milieu de l'image au centre du canvas

    _thread.start_new_thread(movement, ( )) #Les déplacements sont calculés dans un autre thread (=coeur du processeur)

    while rendering:
        """ Le rendu 3D est fait ici """
        
        canvas3D.delete("cube") #On remet l'image à 0
        face_list=[] #Contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), int(couleur), int(profondeur) ], [ (x,y),...], ...]
        #On calcule comment dessiner chaque cube
        for obj in objects : #pour chaque objet dans la liste des objets
            obj_faces=[]
            for face in obj.faces: #pour chaque face de l'objet
                depth = 0
                face_points = [] #Contient 4 sommets à connecter -> (x,y),(x,y),(x,y),(x,y)
                for x,y,z in (obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]], obj.vertices[face[3]]): #pour chaque point de la face, dont la position est constituée de 3 coordonnées : x,y,z
                    #La caméra est à l'origine des axes. Ce sont les objets qui se déplacent et non la caméra.
                    x-=cam.pos[0]
                    y-=cam.pos[1]
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
                    if not -sWidth<X<width+sWidth or not -sHeight<Y<height+sHeight :
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
            #On ajoute les faces de l'objet à la liste de toutes les faces en ne gardant que les trois faces les plus proches, les trois autres étant cachées par les trois premières 
            face_list.append(obj_faces[-3:])
        #On trie les objets selon la "distance" d'une de ses faces choisie arbitrairement (de la plus grande à la plus petite)
        face_list.sort(key=lambda x: x[0][-1], reverse=True)
        #On dessine les objets/faces :
        for obj_faces in face_list:
            for face in obj_faces :
                canvas3D.create_polygon(face[:-1], fill="#ffffff", outline="black", tag="cube")
        root3D.update()
    #fin du "While"
    root3D.destroy() #on ferme la fenêtre


def newLine(board) :
    global realTime, objects
    #self.objects = [ Cube((X,0,Y), board[Y][X], True) if X!=0 and Y!=0 and X!=len(board[0])-1 and Y!=len(board)-1 else Cube((X,0,Y), board[Y][X])   for X in range(len(board[0])) for Y in range(len(board)) ]
    if realTime :
        objects = [ Cube((X,0,Y)) for X in range(len(board[0])) for Y in range(len(board)) if board[Y][X] ]


def launchWindow():
    "Lance la fenêtre du jeu de la vie en 3D"
    global rendering
    rendering=True
    _thread.start_new_thread(window_mainloop, ( )) #on attend pas la fin de l'exécution de window_mainloop


def initialise(in_height, in_width):
    global height, width, cam, sWidth, sHeight
    height = in_height
    width = in_width
    sWidth, sHeight = int(width/2), int(height/2)


pressedkeys = []
objects = []
rendering=False
keys = ('w','a','s','d','q','e')
realTime=True
height, width = 500, 600
sHeight, sWidth = 250, 300
cam = Camera()