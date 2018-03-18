import tkinter
from PIL import ImageTk, Image
import math, random
import time
import os
import _thread

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
    sensRot = 1/40 #sensibilite de la rotation
    # import time as time
    global cos, sin
    while(1):
        time.sleep(0.01)
        for key in pressedkeys:
            cos = (math.cos(cam.rot[0]), math.cos(cam.rot[1]))
            sin = (math.sin(cam.rot[0]), math.sin(cam.rot[1]))

            x,y = sin[1]*sensMouv, cos[1]*sensMouv
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
                root.destroy()

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

        global objects
        for obj in objects :
            obj.show = False
            #On calcule la position du centre de chaque objet pour determiner si il doit etre affiché et dans quel ordre il doit etre dessiné
            x,y,z = obj.pos    
            x-=cam.pos[0]
            y-=cam.pos[1]
            z-=cam.pos[2]

            x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1]   #x et z modifies par la rotation autour de y
            y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0]   #y et z modifies par la rotation autour de x

            if z>0:
                #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
                f=SWidth/z #coefficient de stereoscopie 
                X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

                if X<WIDTH+SWidth and Y<HEIGHT+SHeight and X>-SWidth and Y>-SHeight: #peu d'impact sur framerate
                    obj.show = True







class FloorPannel:
    vertices = (1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1)
    #edges = (0,1),(1,2),(2,3),(3,0)
    faces = ((0,1,2,4),) #un obj a besoin de 2 faces minimum
    depth=0
    show=True
    def __init__(self, position=(0,0,0), color="white"):
        x,y,z = position
        self.pos = position
        self.vertices = [(x+X/2, y+Y/2, z+Z/2) for X,Y,Z in self.vertices]
        self.color=color
        

class Ext3DModel:
    vertices = []
    faces = []          #self.faces = ( ((v,v,v,...),(vn,vn,vn,...)), ((v,v,v,...),(vn,vn,vn,...)), ..... )
    normals = []
    #depth=0
    show=True
    def __init__(self, fileName, position=(0,0,0), color="white", fileOindex=1):
        '''Créé un objet à partir d\'un fichier .obj.'''

        # https://fr.wikipedia.org/wiki/Objet_3D_(format_de_fichier)
        # o = objet        v = vertices           f = faces           les vt, vn et autres ne sont pas lus
        F = open(".\\files\\"+ fileName +".obj","r")
        oNumber=0
        for line in F:
            if line[0] == "o" and line[1] == " " and oNumber<fileOindex: 
                oNumber+=1
            elif line[0] == "v" and line[1] == " " and (oNumber==fileOindex or oNumber==0):
                arr=[]
                vertices = line[1:].split()
                for vertex in vertices:
                    arr.append(float(vertex))
                self.vertices.append(tuple( arr ))
            elif line[0] == "v" and line[1] == "n" and (oNumber==fileOindex or oNumber==0):
                arr=[]
                ass = line[2:].split()
                for fuck in ass:
                    arr.append(float(fuck))
                self.normals.append(tuple( arr ))
            elif line[0] == "f" and line[1] == " " and (oNumber==fileOindex or oNumber==0):
                arr_line = line[1:].split() #arr_line = [v/vt/vn],[v,vt,vn],[v,vt,vn],...
                face_vertices=[]
                face_normals=[]
                for str_face in arr_line:               #str_face = v/vt/vn
                    arr_v_vt_vn = str_face.split("/")   #arr_v_vt_vn = [v,vt,vn]                         contient littéralement les infos des points, textures et normales
                    face_vertices.append( int(arr_v_vt_vn[0]) )
                    face_normals.append( int(arr_v_vt_vn[2]) )

                result = (tuple(face_vertices), tuple(face_normals)) #result = ((v,v,v,...),(vn,vn,vn,...))
                self.faces.append( result )                          #self.faces = ( ((v,v,v,...),(vn,vn,vn,...)), ((v,v,v,...),(vn,vn,vn,...)), .... )
            elif line[0] == "o" and line[1] == " ":
                global objects, colors
                objects.append(Ext3DModel(fileName, position, random.choice(colors), fileOindex+1 ))
                #TODO = create another object
                print("fuck off")
                break
        x,y,z = position
        self.pos = position
        self.vertices = [(x+X/2, y+Y/2, z+Z/2) for X,Y,Z in self.vertices]
        self.color=color



if __name__ == '__main__':
    WIDTH = 1000
    HEIGHT = 1000
    SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
    colors  = ((167,0,0), (0,200,0), (0,0,108), (20,100,230), (50,150,50))
    cam = Camera((0,0,-3)) #position initiale de la caméra

#Crétation de la liste des objets à afficher
    objects = [] 
    ############################## 
    # for x in range(-5, 5):
    #     for z in range(-5, 5):
    #         objects.append(FloorPannel((x,0,z),(255,255,255)))
    ###############################

    #objects.extend([ Ext3DModel("cube",(x,y,z),random.choice(colors)) for y in range(0,-3,-1) for z in range(0,3,1) for x in range(0,3,1)  ])
    #objects.extend([ Ext3DModel("cube_big",(x,y,z),random.choice(colors)) for y in range(0,-4,-2) for z in range(0,4,2) for x in range(0,4,2)  ])
    #objects.extend( [Ext3DModel("cube",(0,0,0),((255,255,255))), Ext3DModel("cube",(2,0,0), (0,0,255)), Ext3DModel("cube",(-2,0,0), (0,255,0))] )        
    objects.append(Ext3DModel("body_highpoly",(1,1,1),(255,255,255) ))



    ##Création de la fenetre
    root = tkinter.Tk()
    frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

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


    #car movement() utilise cos et sin :
    cos = (0,0)
    sin = (1,1)

    _thread.start_new_thread(movement, ( ))
    i,frameRate=0,0
    while True:
        t0 = time.time()

  

        face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]
        #on calcule comment dessiner chaque cube        
        for obj in objects :
            if obj.show:
                for face in obj.faces:
                    depth = 0
                    face_points = [] #contient 3 ou plus sommets a connecter -> (x,y),(x,y),(x,y)

                    #obj.faces = ( ((v,v,v,...),(vn,vn,vn,...)), ((v,v,v,...),(vn,vn,vn,...)),..... )
                    #face = ((v,v,v,...),(vn,vn,vn,...))
                    #face[0] =  (v,v,v,...) = liste des points à connecter, face[1]= (vn,vn,vn,...) = liste des normales
                    for vertid in face[0]:
                        #le monde bouge par rapport a la camera et non le contraire
                        x,y,z = obj.vertices[vertid-1][0] - cam.pos[0], obj.vertices[vertid-1][1]-cam.pos[1], obj.vertices[vertid-1][2]-cam.pos[2]

                        x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1] #x et z modifies par la rotation autour de y
                        y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0] #y et z modifies par la rotation autour de x

                        if not z>0:
                            #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
                            face_points=None
                            break
                        
                        f=SWidth/z #coefficient de stereoscopie 
                        X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D ; +SWidth et SHeight car le repere xyz est placé au milieu de l'ecran
                        if not -50<X<WIDTH+50 or not -50<Y<HEIGHT+50 : #peut etre ajuste pour les performances
                            #on affiche pas ce qui est hors champ
                            face_points=None
                            break
                        
                        face_points.append((X,Y)) 
                        depth += (x**2)+(y**2)+(z**2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D     

                    if face_points is not None:
                        #si il n'y a pas 1 ou des points qui sort de l'écran

                        #Calcule shaders
                        nz = sum( [obj.normals[face[1][n] -1][2] for n in range( len(face[1])-1 )  ] ) / (len(face[1])-1) + 0.2 #moyenne des coordonnes "z" des normales, +0.2 pour eviter d'avoir des endroits avec 0 lumiere
                        
                        faceColor = tuple([ 5 if colorComponent*nz<5. else 255 if colorComponent*nz>255. else int(colorComponent*nz) for colorComponent in obj.color ])
                        ######
                        face_points.extend( (faceColor, depth) ) #face_points[4] est dedié à la couleur ; face_point[5] dedié à la profondeur
                        face_list.append(face_points)
        
        
        face_list.sort(key=lambda x: x[-1], reverse=True)
        for face in face_list:
            canvas.create_polygon(face[:-2], fill='#%02x%02x%02x' % face[-2], tag="faces") #la couleur est transformée de RGB en hexadecimal


        root.update()
        canvas.delete("faces")

        frameRate += time.time()-t0
        i+=1
        if i > 50 :
            print(1/((frameRate/i)+1e-10),"fps")
            i=0
            frameRate=0
