import tkinter
import PIL
from PIL import ImageTk, Image, ImageDraw
import time
import math

WIDTH = 800
HEIGHT = 800
SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
sensMouv = 0.25 #sensibilite des mouvements
sensRot = 1/15 #sensibilite de la rotation



class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

def rotate(pos, rotation):
    a,z=pos #a est x ou y
    sin=math.sin(rotation)
    cos=math.cos(rotation)
    #return z*cos+a*cos, z*sin-x*sin
    return a*cos-z*sin, z*cos+a*sin

def keypress(event):
    #deplacement
    #right left forward backward  up  down
    # --X  ++X    ++Z     --Z    ++Y  --Y
    if event.keysym == 'd':
        cam.pos[0]-=sensMouv
    elif event.keysym == 'a':
        cam.pos[0]+=sensMouv
    elif event.keysym == 'w':
        cam.pos[2]+=sensMouv
    elif event.keysym == 's':
        cam.pos[2]-=sensMouv
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
        cam.rot[1]+=sensRot
    elif event.keysym == 'Right':
        cam.rot[1]-=sensRot
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





#sommets du cube selon le repere (x,y,z) puis les arretes du cube
vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4)

cam=Camera((0,0,-5))
i=0
while True:
    t0 = time.time()
    # chaque frame sera PILimg
    PILimg = Image.new('RGB', (WIDTH,HEIGHT), (255,255,255))
    

    
    #position de ces sommets sur l'image 2D
    verticesPxPos = []

    draw = ImageDraw.Draw(PILimg)
    for edge in edges:
        points = [] #contient 2 sommets a connecter par arrete
        for x,y,z in (vertices[edge[0]], vertices[edge[1]]):
            #le monde bouge par rapport a la camera et non le contraire
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            x,z = rotate((x,z),cam.rot[1]) #x et z modifies par la rotation autour de y
            y,z = rotate((y,z),cam.rot[0]) #y et z modifies par la rotation autour de x
            
            f=SWidth/(z+0.0001) #un coefficient de stereoscopie,    

            x,y = int(x*f)+SWidth, int(y*f)+SHeight #position des sommets sur l'image 2D

            #x et y doivent cerrespondre a des pixels du canvas !
            x = clamp(x,0,WIDTH)
            y = clamp(y,0,HEIGHT)
            
            points.append([x,y]) 
            #PILimg.putpixel ((x,y), ( 255, 0, 0 )) #on met les sommets
        draw.line((points[0][0],points[0][1], points[1][0],points[1][1]), fill=128)
    del draw


    img = ImageTk.PhotoImage(PILimg)
    oneFrame = canvas.create_image(SWidth, SHeight, image=img) #jsp pq faut utiliser SW et SH

    root.update()
    canvas.delete(oneFrame)
    t1 = time.time()
    print(1/(t1-t0),"fps")
root.mainloop() #end
