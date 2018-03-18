import tkinter
import PIL
from PIL import ImageTk, Image, ImageDraw
import time
import math, random

WIDTH = 1000
HEIGHT = 1000
SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
sensMouv = 0.25 #sensibilite des mouvements
sensRot = 1/7 #sensibilite de la rotation
colors  = ["red","green","blue","orange","purple","pink","yellow"]


class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

def rotate(pos, rotation):
    a,z=pos #a represente x ou y en fonction des cas 
    sin=math.sin(rotation)
    cos=math.cos(rotation)
    return a*cos-z*sin, z*cos+a*sin

def keypress(event):
    #deplacement
    x,y = math.sin(cam.rot[1]), math.cos(cam.rot[1])
    
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
    
    
def clamp (val, minval, maxval):
    "retourne val, compris entre minval et maxval"
    if val < minval: return minval
    if val > maxval: return maxval
    return val

##Création de la fenetre
root = tkinter.Tk()
frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
root.bind("<Key>", keypress)
frame.pack()




#sommets du cube selon le repere (x,y,z) puis les arretes du cube, puis ses faces
vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4)
faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)

cam=Camera((0,0,-6))


while True:
    # chaque frame sera PILimg
    PILimg = Image.new('RGB', (WIDTH,HEIGHT), (0,0,0))
    

    #### Création d'une liste de faces et leur profondeur
    face_list=[] #contient : [points1, points2, ...] => [ [ [x,y],[x,y],[x,y],[x,y] ], [ [x,y],...], ...]
    depth_list=[]
    for face in faces:
        depth = 0
        face_points = [] #contient 4 sommets a connecter
        for x,y,z in (vertices[face[0]], vertices[face[1]], vertices[face[2]], vertices[face[3]]):
            #le monde bouge par rapport a la camera et non le contraire
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            x,z = rotate((x,z),cam.rot[1]) #x et z modifies par la rotation autour de y
            y,z = rotate((y,z),cam.rot[0]) #y et z modifies par la rotation autour de x
            
            f=SWidth/(z+0.0001) #un coefficient de stereoscopie, z pas egal a 0 donc pas de division par 0    

            x,y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

            #x et y doivent cerrespondre a des pixels du canvas ! (on evite le index out of range)
            #TODO changer ça pour un truc qui fonctionne vraiment
            x = clamp(x,0,WIDTH)
            y = clamp(y,0,HEIGHT)

            face_points.append([x,y]) 
            depth += z**4 #on exacèrbe la profondeur, TODO ne pa la calculer que a partir de z
        
        face_points.append([colors[faces.index(face)]]) #points[4][0] est dedié à la couleur
        depth_list.append(depth)
        face_list.append(face_points)

    #dessiner faces
    face_list=[x for _,x in sorted(zip(depth_list,face_list), reverse=True)] #on ordonne face_list selon l'ordre de depth_list
    draw = ImageDraw.Draw(PILimg)
    for face in face_list :
        color=face[4][0]
        draw.polygon((tuple(face[0]),tuple(face[1]),tuple(face[2]),tuple(face[3])), fill=color, outline="black")
    del draw

    #afficher image
    img = ImageTk.PhotoImage(PILimg)
    oneFrame = canvas.create_image(SWidth, SHeight, image=img) #SWidth et SHeight servent a mettre le milieu de l'image au centre du canvas

    root.update()
    canvas.delete(oneFrame)
