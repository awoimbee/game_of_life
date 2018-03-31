import tkinter
from PIL import ImageTk, Image
import math, random
import os
import _thread
import time

WIDTH = 1000
HEIGHT = 1000
SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height

colors  = ("#000000", "#FFFFFF", "#6D8572", "#FAE705", "#343A83", "#00FF00", "#FFB400", "#AD009E", "#ADF097")
pressedkeys=[]

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

def keydown(event):
    if event.keysym not in pressedkeys:
        pressedkeys.append(event.keysym)

def keyup(event):
    if event.keysym in pressedkeys:
        pressedkeys.pop(pressedkeys.index(event.keysym))

def movement():
    """Calcule le déplacement et l'ordre d'affichage des objets en fonction de l'input."""

    sensMouv = 1/10 #sensibilite des mouvements
    sensRot = 1/30 #sensibilite de la rotation
    
    while(1):
        time.sleep(0.01)
        for key in pressedkeys:
            x,y = math.sin(cam.rot[1])*sensMouv, math.cos(cam.rot[1])*sensMouv
            if key == 'd':
                cam.pos[0]+=y
                cam.pos[2]-=x
            elif key == 'a':
                cam.pos[0]-=y
                cam.pos[2]+=x
            elif key == 'w':
                cam.pos[0]+=x
                cam.pos[2]+=y
            elif key == 's':
                cam.pos[0]-=x
                cam.pos[2]-=y

            elif key == 'q':
                cam.pos[1]+=sensMouv
            elif key == 'e':
                cam.pos[1]-=sensMouv

            #exit
            elif key == 'Escape':
                _thread.interrupt_main() #c'est pas fou comme solution

            #rotation
            # axe X     axe Y
            # rot[1]    rot[0]
            elif key == 'Left':
                cam.rot[1]-=sensRot
            elif key == 'Right':
                cam.rot[1]+=sensRot
            elif key == 'Up':
                cam.rot[0]-=sensRot
            elif key == 'Down':
                cam.rot[0]+=sensRot
        ##########################################################
        # REVOVE NOT SHOWED OBJECTS
        #mettre ça ici permet d'améliorer le framerate
        #on calcule dans quel ordre dessiner chaque cube - *on retire ceux qui sont hors champ*
        global objects
        for obj in objects :
            obj.show = False
            #On calcule la position du centre de chaque objet pour determiner si il doit etre affiché et dans quel ordre il doit etre dessiné
            x,y,z = obj.pos    
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            x,z = rotate2D((x,z),cam.rot[1]) #x et z modifies par la rotation autour de y
            y,z = rotate2D((y,z),cam.rot[0]) #y et z modifies par la rotation autour de x

            if z>0:
                #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
                f=SWidth/z #coefficient de stereoscopie 
                X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

                if X<WIDTH and Y<HEIGHT and X>0 and Y>0: #peu d'impact sur framerate
                    obj.depth = (x**2)+(y**2)+(z**2)
                    #print(obj.depth, obj.color, "pos :", x,y,z)
                    obj.show = True

        objects.sort(key=lambda x: x.depth, reverse=True) #on ordonne objects selon l'ordre de depth
        ############################################################# impact *très minime* sur le framerate



def rotate2D(pos, rotation):
    #pos[0] represente x ou y en fonction des cas, pos[1]=z
    sin=math.sin(rotation)
    cos=math.cos(rotation)
    return pos[0]*cos-pos[1]*sin, pos[1]*cos+pos[0]*sin


def gameOfLife(objects, objNb):
    while(1):
        time.sleep(0.1)

        for x in range(len(objects)):
            for y in range(len(objects[x])):
                for z in range(len(objects[x][y])):

                    """
                    A cyclic cellular automaton is defined as an automaton where each cell takes one of N states 0 , 1 , 2 , ...N − 1 and a cell in state i changes to state i + 1 mod N at  the  next  time  step  if  it  has  a  neighbor  that  is  in  statei + 1 mod N, otherwise it remains in state i at the next time step.
                    """
##                    nextState = (objects[x][y][z].life+1)%4
                    r1, r2, r3, r4 = 1, 7, 9, 15
                    life_sum = 0
                    for i in range(-1, 2):
                        for j in range(-1,2):    
                            for k in range(-1, 2):
                                if not (i==0 and j==0 and k==0):
                                    life_sum += objects [(x+i)%len(objects)] [(y+j)%len(objects[x])] [(z+k)%len(objects[x][y])] .life
##                                    if objects [(x+i)%len(objects)] [(y+j)%len(objects[x])] [(z+k)%len(objects[x][y])] .life == nextState:
##                                        objects[x][y][z].life = nextState
##                                        nextState = (objects[x][y][z].life+1)%4

                    objects[x][y][z].life = (life_sum*2)%9

class Object:
    ''' Classe représentant tous les objets '''
    depth=0
    show=False

    def __init__(self, position=(0,0,0), life=0):
        x,y,z = position
        self.pos = position
        #on calcule les coordonnees de chaque arrete du cube en fonction de ses dimensions et sa position dans l'espace
        # X,Y,Z = un point de l'objet
        self.vertices = [(x+X, y+Y, z+Z) for X,Y,Z in self.vertices]
        #jsp pas pq faut diviser par 2 mais ça fonctionne mieux <- ça change juste les dimensions des objets
        self.life=life

class Cube(Object):
    #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses arretes, puis ses faces
    vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
    #edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4) #ne sert a rien
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)

    def __init__(self, position=(0,0,0), color="white"):
        Object.__init__(self, position, color)

class FloorPannel(Object):
    vertices = (1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1)
    faces = ((0,1,2,3),(0,1,2,3),(0,1,2,3),(0,1,2,3) ) #Dirty patch, c'est à cause de "face_list.extend(obj_faces[3:])" plus bas

    def __init__(self, position=(0,0,0), color="white"):
        Object.__init__(self, position, color)
        

##Création de la fenetre
root = tkinter.Tk()
frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
#création du canvas et paramétrage de la récupération de l'entrée utilisateur
canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)

frame.pack()

##Fond d'ecran
current_file_dir = os.path.dirname(__file__)
img_path = os.path.join(current_file_dir, "./files/Synthwave-Neon-80s-Background-4K.jpg")
img = Image.open(img_path)
x, y = int(HEIGHT*(16/9)), HEIGHT
img = img.resize((x,y))
tkimg = ImageTk.PhotoImage(img)
canvas.create_image(SWidth, SHeight, image=tkimg) #SWidth et SHeight servent a mettre le milieu de l'image au centre du canvas
#####

#Création de la caméra
cam = Camera((0,0,-6))

#Création des objets à afficher
objects_3D = [] 
#objects.extend([ FloorPannel((x,0,z),"white") for z in range(-5,5) for x in range(-5,5) ])
objects_3D.extend([ [[Cube((x,y,z), random.choice([0,1,2,3,4])) for x in range(0,-20,-4)] for y in range(0,20,4)] for z in range(0,20,4)  ]) #liste 3D pour le jeu de la vie
objects = [obj for dimension1 in objects_3D for dimension2 in dimension1 for obj in dimension2] # liste 2D pour le rendu 3d


i,frameRate=0,0
_thread.start_new_thread(movement, ( )) #les déplacements sont calculés dans un autre thread
_thread.start_new_thread(gameOfLife, (objects_3D, len(objects) ))
while True:
    t0 = time.time()


    face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]
    
    #on calcule comment dessiner chaque cube
    for obj in objects :
        if obj.show and obj.life>0 :

            obj_faces=[]
            for face in obj.faces:
                
                depth = 0
                face_points = [] #contient 4 sommets a connecter -> (x,y),(x,y),(x,y),(x,y)
                for x,y,z in (obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]], obj.vertices[face[3]]):
                    #le monde bouge par rapport a la camera
                    x-=cam.pos[0]
                    y-=cam.pos[1]
                    z-=cam.pos[2]

                    x,z = rotate2D((x,z),cam.rot[1]) #x et z modifies par la rotation autour de y
                    y,z = rotate2D((y,z),cam.rot[0]) #y et z modifies par la rotation autour de x


                    f=SWidth/z #coefficient de stereoscopie
                    X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D ; +SWidth et SHeight car le repere xyz est placé au milieu de l'ecran

                    face_points.append((X, Y)) #position en pixels des sommets sur l'image 2D
                    depth += (x**2)+(y**2)+(z**2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D

                face_points.extend( (depth, ) )
                    #face_points[4] est dedié à la couleur, cela permet une meilleure optimisation (20fps au lieu de 10!)
                    #face_point[5] dedié à la profondeur
                obj_faces.append(face_points)

            obj_faces.sort(key=lambda x: x[-1], reverse=True)
            for face in obj_faces[-3:]: #on ne dessine que les 3 faces maximum visibles simultanément
                #print(face[-2], colors())
                canvas.create_polygon(face[:-1], fill=colors[obj.life], outline="black", tag="face")


    root.update()
    canvas.delete("face") #on remet l'image à 0

    frameRate += time.time()-t0
    i+=1
    if i > 50 :
        print(1/((frameRate/i)+1e-10),"fps")
        i=0
        frameRate=0
