import tkinter
from PIL import ImageTk, Image
import math, random
import time
import os

WIDTH = 1000
HEIGHT = 1000
SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
sensMouv = 1/5 #sensibilite des mouvements
sensRot = 1/10 #sensibilite de la rotation

colors  = ("#6D8572", "#FAE705", "#343A83", "#00FF00", "#FFB400", "#AD009E")

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

def keypress(event):
    """Calcule le déplacement et l'ordre d'affichage des objets en fonction de l'input."""
    #deplacement
    global cos, sin
    x,y = sin[1]*sensMouv, cos[1]*sensMouv
    if event.keysym == 'd':
        cam.pos[0]+=y
        cam.pos[2]-=x
    elif event.keysym == 'a':
        cam.pos[0]-=y
        cam.pos[2]+=x
    elif event.keysym == 'w':
        cam.pos[0]+=x
        cam.pos[2]+=y
    elif event.keysym == 's':
        cam.pos[0]-=x
        cam.pos[2]-=y

    elif event.keysym == 'q':
        cam.pos[1]+=sensMouv
    elif event.keysym == 'e':
        cam.pos[1]-=sensMouv

    #exit
    elif event.keysym == 'Escape':
        root.destroy()

    #rotation
    # axe X     axe Y
    # rot[1]    rot[0]
    elif event.keysym == 'Left':
        cam.rot[1]-=sensRot
    elif event.keysym == 'Right':
        cam.rot[1]+=sensRot
    elif event.keysym == 'Up':
        cam.rot[0]-=sensRot
    elif event.keysym == 'Down':
        cam.rot[0]+=sensRot


    ##########################################################
    # REVOVE NOT SHOWED OBJECTS
    #mettre ça ici permet d'améliorer le framerate
    #on calcule dans quel ordre dessiner chaque cube - *on retire ceux qui sont hors champ*
    global objects
    for obj in objects :
        obj.show = False
        x,y,z = obj.pos     #tout cela est calculé à partir du centre de chaque cube
        x-=cam.pos[0]
        y-=cam.pos[1]
        z-=cam.pos[2]

        x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1]   #x et z modifies par la rotation autour de y
        y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0] #y et z modifies par la rotation autour de x

        if z>0:
            #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
            f=SWidth/z #coefficient de stereoscopie 
            X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

            if X<WIDTH+SWidth and Y<HEIGHT+SHeight and X>-SWidth and Y>-SHeight: #peu d'impact sur framerate
                obj.depth = (x**2)+(y**2)+(z**2)
                obj.show = True
    ############################################################# super fast



class Cube:
    #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses arretes, puis ses faces
    vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
    #edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4) #ne sert a rien
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
    depth=0
    show=False

    def __init__(self, position=(0,0,0), color="white"):
        x,y,z = position
        self.pos = position
        #on calcule les coordonnees de chaque arrete du cube en fonction de ses dimensions et sa position dans l'espace
        # X,Y,Z = un point de l'objet
        self.vertices = [(x+X/2, y+Y/2, z+Z/2) for X,Y,Z in self.vertices]
        #jsp pas pq faut diviser par 2 mais ça fonctionne mieux
        self.color=color

class FloorPannel:
    vertices = (1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1)
    #edges = (0,1),(1,2),(2,3),(3,0)
    faces = ((0,1,2,3), ) #un obj a besoin de 2 faces minimum
    depth=0
    show=False
    def __init__(self, position=(0,0,0), color="white"):
        x,y,z = position
        self.pos = position
        self.vertices = [(x+X/2, y+Y/2, z+Z/2) for X,Y,Z in self.vertices]
        self.color=color
        

##Création de la fenetre
root = tkinter.Tk()
frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
root.bind("<Key>", keypress)
frame.pack()

##Fond d'ecran
current_file_dir = os.path.dirname(__file__)
img_path = os.path.join(current_file_dir, "./files/Synthwave-Neon-80s-Background-4K.jpg")
img = Image.open(img_path)
x, y = int(HEIGHT*(16/9)), HEIGHT
img = img.resize((x,y))
tkimg = ImageTk.PhotoImage(img)
canvas.create_image(SWidth, SHeight, image=tkimg) #SWidth et SHeight servent a mettre le milieu de l'image au centre du canvas


#Création de la fenetre et des objets
cam = Camera((0,0,-6))

objects = [] 
############################## 
for x in range(-5, 5):
    for z in range(-5, 5):
        objects.append(FloorPannel((x,0,z),"white"))
###############################
##objects = []  
for x in range(0,20,2):
    for z in range(0,20,2):
        for y in range(0,-6,-2):
            objects.append(Cube((x,y,z),random.choice(colors)))

##objects.extend( [Cube((0,0,0),"red"),Cube((2,0,0), "blue"), Cube((-2,0,0), "yellow")])        

i,frameRate=0,0
while True:
    t0 = time.time()

    cos = (math.cos(cam.rot[0]), math.cos(cam.rot[1]))
    sin = (math.sin(cam.rot[0]), math.sin(cam.rot[1]))
    
    objects.sort(key=lambda x: x.depth, reverse=True) #on ordonne objects selon l'ordre de depth
    #on affiche pas les objets les plue eloignes
    crop = int(len(objects)/10)
    #on calcule comment dessiner chaque cube
    for obj in objects[crop:] :
        if obj.show :
            face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]
            for face in obj.faces:
                
                depth = 0
                face_points = [] #contient 4 sommets a connecter -> (x,y),(x,y),(x,y),(x,y)
                for x,y,z in (obj.vertices[face[0]], obj.vertices[face[1]], obj.vertices[face[2]], obj.vertices[face[3]]):
                    #le monde bouge par rapport a la camera et non le contraire
                    x-=cam.pos[0]
                    y-=cam.pos[1]
                    z-=cam.pos[2]

                    x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1] #x et z modifies par la rotation autour de y
                    y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0] #y et z modifies par la rotation autour de x

                    if z>0:
                        f=SWidth/z #coefficient de stereoscopie 
                        face_points.append((x*f+SWidth, y*f+SHeight)) #position en pixels des sommets sur l'image 2D
                        depth += (x**2)+(y**2)+(z**2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D
                if len(face_points) > 1:
                    #si il y a au moins 2 points à connecter
                    face_points.extend( (obj.color, depth) )
                    #face_points[4] est dedié à la couleur, cela permet une meilleure optimisation (20fps au lieu de 10!)
                    #face_point[5] dedié à la profondeur
                    face_list.append(face_points)
        
            ##DO THE DRAWING HERE
            face_list.sort(key=lambda x: x[-1], reverse=True)
            for face in face_list[-3:]: #on ne dessine que les 3 faces maximum visibles simultanément
                canvas.create_polygon(face[:-2], fill=face[-2], outline="black", tag="face")


    root.update()
    #on remet l'image à 0

    ##tLOL = time.time()
    canvas.delete("face")
    ##print(( time.time()-tLOL ), "canvas delete")

    frameRate += time.time()-t0
    i+=1
    if i > 50 :
        print(1/((frameRate/i)+1e-10),"1/fps")
        i=0
        frameRate=0
