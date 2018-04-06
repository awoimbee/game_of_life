import tkinter
from PIL import ImageTk, Image
import math, random
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
    """Calcule le déplacement de la camera"""
    sensMouv = 1/10 #sensibilite des mouvements
    sensRot = 1/30 #sensibilite de la rotation
    
    while(1):
        time.sleep(0.01)
        for key in pressedkeys:
            #déplacement
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

            #rotation
            # axe X  |  axe Y
            # rot[1] |  rot[0]
            elif key == 'Left':
                cam.rot[1]-=sensRot
            elif key == 'Right':
                cam.rot[1]+=sensRot
            elif key == 'Up':
                cam.rot[0]-=sensRot
            elif key == 'Down':
                cam.rot[0]+=sensRot

            elif key == 'Escape':
                _thread.interrupt_main() #exit


def rotate2D(vertex, rotation):
    """Rotation en 2 dimensions de l'axe partant de l'origine vers le point "vertex" """
    #https://www.siggraph.org/education/materials/HyperGraph/modeling/mod_tran/2drota.htm
    sin=math.sin(rotation)
    cos=math.cos(rotation)
    return vertex[0]*cos-vertex[1]*sin, vertex[1]*cos+vertex[0]*sin


def gameOfLife(objects, objNb):
    """ PLACEHOLDER """
    while(1):
        time.sleep(0.1)

        for x in range(len(objects)):
            for y in range(len(objects[x])):
                for z in range(len(objects[x][y])):

                    """
                    A cyclic cellular automaton is defined as an automaton where each cell takes one of N states 0 , 1 , 2 , ...N − 1 and a cell in state i changes to state i + 1 mod N at  the  next  time  step  if  it  has  a  neighbor  that  is  in  statei + 1 mod N, otherwise it remains in state i at the next time step.
                    """
##                   nextState = (objects[x][y][z].life+1)%4
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



class Cube:
    #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses faces
    vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
    depth=0
    
    def __init__(self, objPos=(0,0,0), life=0):
        self.pos = objPos
        #on calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(objPos[0]+X, objPos[1]+Y, objPos[2]+Z) for X,Y,Z in self.vertices]
        self.life=life


##Création de la fenetre
root = tkinter.Tk()
frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
#création du canvas et paramétrage de la récupération de l'entrée utilisateur
canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg="#343D46")
canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
root.bind("<KeyPress>", keydown)
root.bind("<KeyRelease>", keyup)

frame.pack()

##Fond d'ecran
img = Image.open("./background.jpg")
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
objects_3D.extend([ [[Cube((x,y,z), random.choice([0,1,2,3,4])) for x in range(0,-40,-4)] for y in range(0,4,4)] for z in range(0,40,4)  ]) #liste 3D pour le jeu de la vie
objects = [obj for dimension1 in objects_3D for dimension2 in dimension1 for obj in dimension2] # liste 1D pour le rendu 3d


i,frameRate=0,0
_thread.start_new_thread(movement, ( )) #les déplacements sont calculés dans un autre thread
_thread.start_new_thread(gameOfLife, (objects_3D, len(objects) ))
while True:
    t0 = time.time()

    face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]

    #on calcule comment dessiner chaque cube
    for obj in objects :
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

                if z<=0:
                    #on affiche pas ce qui est hors champ
                    face_points = None
                    break

                f=SWidth/z #coefficient de stereoscopie
                X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D ; +SWidth et +SHeight car le repere xyz est placé au milieu de l'ecran

                if not 0<X<WIDTH or not 0<Y<HEIGHT :
                    #on affiche pas ce qui est hors champ
                    face_points = None
                    break

                face_points.append((X, Y)) #position en pixels des sommets sur l'image 2D
                depth += (x**2)+(y**2)+(z**2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D

            if face_points is None:
                #on arrete decalculer les faces de l'objet
                break
            face_points.extend( (obj.life, depth) ) #face_points contient les coordonnees des points de la face, mais aussi la couleur et profondeur de la face
            obj_faces.append(face_points)

        obj_faces.sort(key=lambda x: x[-1], reverse=True)
        face_list.extend(obj_faces[-3:]) #[-3:] car on ne dessine que les 3 faces maximum visibles simultanément

    face_list.sort(key=lambda x: x[-1], reverse=True)
    #On dessine les faces :
    for face in face_list:
        canvas.create_polygon(face[:-2], fill=colors[face[-2]], outline="black", tag="face")


    root.update()
    canvas.delete("face") #on remet l'image à 0

    frameRate += time.time()-t0
    i+=1
    if i > 50 :
        print(1/((frameRate/i)),"fps")
        i=0
        frameRate=0
