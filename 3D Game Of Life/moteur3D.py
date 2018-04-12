import tkinter
from PIL import ImageTk, Image
import math, random
import _thread
import time

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

class Cube:
    #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses faces
    vertices = (-0.5,0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,-0.5), (-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5),(-0.5,-0.5,0.5)
    faces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
    life = int()    
    def __init__(self, pos=(0,0,0), life=0):
        #on calcule les coordonnees de chaque point du cube en fonction de sa position à l'origine et de la position de l'objet dans l'espace
        self.vertices = [(pos[0]+X, pos[1]+Y, pos[2]+Z) for X,Y,Z in self.vertices]
        self.life=life

def RenderingIn3D(cam, objects,  height, width) :
    pressedkeys = []
    sWidth, sHeight = int(width/2), int(height/2)

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
        
        while(True):
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


    root = tkinter.Tk()
    frame = tkinter.Frame(root, width=width, height=height)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    #création du canvas et paramétrage de la récupération de l'entrée utilisateur
    canvas = tkinter.Canvas(frame, width=width, height=height, bg="#343D46")
    canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
    root.bind("<KeyPress>", keydown)
    root.bind("<KeyRelease>", keyup)
    frame.pack()

    _thread.start_new_thread(movement, ( )) #les déplacements sont calculés dans un autre thread
    i,frameRate=0,0
    while True:
        """ Le rendu 3D est fait ici """
        t0 = time.time()

        #TODO : faire un render pour chaque etage
        
        """Fait le rendu d'une seule image"""
        canvas.delete("all") #on remet l'image à 0
        face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), int(couleur), int(profondeur) ], [ (x,y),...], ...]
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
                    f=(width/2)/z #coefficient de stereoscopie
                    X,Y = int(x*f)+sWidth, int(y*f)+sHeight #position en pixels des sommets sur l'image 2D ; +Swidth et +Sheight car le repere xyz est placé au milieu de l'ecran
                    if not 0<X<width or not 0<Y<height :
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
                color = '#ffffff' if face[-2]==True else "#000000" 
                canvas.create_polygon(face[:-2], fill=color, outline="black")


        root.update()
        frameRate += time.time()-t0
        i+=1
        if i > 50 :
            print(1/((frameRate/i)),"fps")
            i=0
            frameRate=0
        
 



    # ##Fond d'ecran
    # img = Image.open("./background.jpg")
    # x, y = int(height*(16/9)), height
    # img = img.resize((x,y))
    # tkimg = ImageTk.PhotoImage(img)
    # canvas.create_image(Swidth, Sheight, image=tkimg) #Swidth et Sheight servent a mettre le milieu de l'image au centre du canvas
    # #####

    


RenderingIn3D(Camera((0,0,-5)), [Cube((x,y,z), random.choice([0,1])) for x in range(0,-40,-1) for y in range(0,8,4) for z in range(0,40,1) ], 700, 900)

