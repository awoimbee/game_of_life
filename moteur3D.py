import tkinter
from PIL import ImageTk, Image
import math, random
import time
import os
import _thread

WIDTH = 1500
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

    elif event.keysym == 'f':
        global fastCoeff
        if fastCoeff <0.7:
            fastCoeff+=0.1
        else :
            fastCoeff=0
        print("rendu rapide niveau", (fastCoeff*100//0.7), "%" )

    ##########################################################
    # REVOVE NOT SHOWED OBJECTS
    #mettre ça ici permet d'améliorer le framerate
    #on calcule dans quel ordre dessiner chaque cube - *on retire ceux qui sont hors champ*
    global objects
    for obj in objects :
        obj.show = False ### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! DEBUG
        #On calcule la position du centre de chaque objet pour determiner si il doit etre affiché et dans quel ordre il doit etre dessiné
        x,y,z = obj.pos    
        x-=cam.pos[0]
        y-=cam.pos[1]
        z-=cam.pos[2]

        x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1]   #x et z modifies par la rotation autour de y
        y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0] #y et z modifies par la rotation autour de x

        if z>0:
            #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
            f=SWidth/z #coefficient de stereoscopie 
            X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

            #if X<WIDTH+SWidth and Y<HEIGHT+SHeight and X>-SWidth and Y>-SHeight: #peu d'impact sur framerate
            obj.depth = (x**2)+(y**2)+(z**2)
            obj.show = True
    ############################################################# impact *très minime* sur le framerate


def clamp (val, minval, maxval):
    "retourne val, compris entre minval et maxval"
    if val < minval: return minval
    if val > maxval: return maxval
    return val


# class Cube: #NEEDS UPDATING
#     #sommets du cube quand il est positionné sur l'origine des reperes x,y,z puis ses arretes, puis ses faces
#     vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
#     #edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4) #ne sert a rien
#     faces = (4,5,6),(4,7,6), (0,3,7),(0,4,7), (1,2,6),(1,5,6), (3,2,6),(3,7,6), (0,1,4),(5,4,1), (0,1,2),(0,3,2)
#     #squarefaces = (4,5,6,7),(0,3,7,4),(1,2,6,5),(3,2,6,7),(0,1,5,4),(0,1,2,3)
#     depth=0
#     show=True

#     def __init__(self, position=(0,0,0), color="white"):
#         x,y,z = position
#         self.pos = position
#         #on calcule les coordonnees de chaque arrete du cube en fonction de ses dimensions et sa position dans l'espace
#         # X,Y,Z = un point de l'objet
#         self.vertices = [(x+X/2, -y-Y/2, -z-Z/2) for X,Y,Z in self.vertices]
#         #jsp pas pq faut diviser par 2 mais ça fonctionne mieux
#         self.color=color

class FloorPannel:
    vertices = (1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1)
    #edges = (0,1),(1,2),(2,3),(3,0)
    faces = ((0,1,2), (0,3,2)) #un obj a besoin de 2 faces minimum
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
    depth=0
    show=True
    def __init__(self, fileName, position=(0,0,0), color="white", fileOindex=0):
        '''Créé un objet à partir d\'un fichier .obj.'''

        # https://fr.wikipedia.org/wiki/Objet_3D_(format_de_fichier)
        # o = objet        v = vertices           f = faces           les vt, vn et autres ne sont pas lus
        F = open(".\\files\\"+ fileName +".obj","r")
        oNumber=-1
        for line in F:
            if line[0] == "o" and line[1] == " " and oNumber<fileOindex: 
                oNumber+=1
            elif line[0] == "v" and line[1] == " ":
                arr=[]
                ass = line[1:].split()
                for fuck in ass:
                    arr.append(float(fuck))
                self.vertices.append(tuple( arr ))
            elif line[0] == "v" and line[1] == "n":
                arr=[]
                ass = line[2:].split()
                for fuck in ass:
                    arr.append(float(fuck))
                self.normals.append(tuple( arr ))
            elif line[0] == "f" and line[1] == " ":
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
                #TODO = create another object
                print("fuck off")
                break
        x,y,z = position
        self.pos = position
        self.vertices = [(x+X/2, -y-Y/2, -z-Z/2) for X,Y,Z in self.vertices]
        self.color=color
        print(self.faces[0])


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
cam = Camera((0,0,-3))

objects = [] 
############################## 
# for x in range(-5, 5):
#     for z in range(-5, 5):
#         objects.append(FloorPannel((x,0,z),(255,255,255)))
###############################
#for x in range(0,20,2):
#    for z in range(0,20,2):
#        for y in range(0,-6,-2):
#            objects.append(Cube((x,y,z),random.choice(colors)))

#objects.extend( [Ext3DModel("cube",(0,0,0),((255,0,0))), Ext3DModel("cube",(2,0,0), (0,0,255)), Ext3DModel("cube",(-2,0,0), (0,255,0))] )        
#objects.append(Ext3DModel("LowPolyPickup",(0,0,0),(255,155,255) ))
for x in range(0,2):
    for z in range(0,2):
        for y in range(0,-2,-1):
            objects.append( Ext3DModel("cube_big",(x,y,z),(255,155,255)) )

i,frameRate=0,0
fastCoeff=0
while True:
    t0 = time.time()

    cos = (math.cos(cam.rot[0]), math.cos(cam.rot[1]))
    sin = (math.sin(cam.rot[0]), math.sin(cam.rot[1]))
    
    objects.sort(key=lambda x: x.depth, reverse=True) #on ordonne objects selon l'ordre de depth
    #on affiche pas les objets les plue eloignes
    
    #on calcule comment dessiner chaque cube
    
    for obj in objects :
        if obj.show :
            # TODO = SKIP SOME POLY WHEN OBJECT IS FAR
            face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]
            for face in obj.faces:
                
                depth = 0
                face_points = [] #contient 3 ou plus sommets a connecter -> (x,y),(x,y),(x,y)

                #obj.faces = ( ((v,v,v,...),(vn,vn,vn,...)), ((v,v,v,...),(vn,vn,vn,...)),..... )
                #face = ((v,v,v,...),(vn,vn,vn,...))
                #face[0] = liste des points à connecter, face[1]=list des normales wtf c'est trop chaud
                for vertid in face[0]:
                    x,y,z = obj.vertices[vertid-1] 
                    #le monde bouge par rapport a la camera et non le contraire
                    x-=cam.pos[0]
                    y-=cam.pos[1]
                    z-=cam.pos[2]

                    x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1] #x et z modifies par la rotation autour de y
                    y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0] #y et z modifies par la rotation autour de x


                    if not z>0:
                        #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
                        face_points=None
                        break
                    
                    f=SWidth/z #coefficient de stereoscopie 
                    X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D ; +SWidth et SHeight car le repere xyz est placé au milieu de l'ecran
                    if not X<WIDTH+50 or not Y<HEIGHT+50 or not X>-50 or not Y>-50: #should be the following, has been cut for performance not X<WIDTH+SWidth and not Y<HEIGHT+SHeight and not X>-SWidth and not Y>-SHeight
                        #on affiche pas ce qui est hors champ
                        face_points=None
                        break
                    
                    face_points.append((X,Y)) 
                    depth += (x**2)+(y**2)+((z**2)*2) #se calcule avec *petit* x,y,z car ils sont position en 3d là où Y,X sont en 2D

                if face_points is not None:
                    #si il n'y a pas au moins 1 des points qui sort de l'écran
                    # bad attempt at simple shading
                    #divider = depth / 300
                    #color = tuple([ int(clamp((val)-divider, 0, 255)) for val in obj.color  ])
                    face_points.extend( (obj.color, depth) ) #face_points[4] est dedié à la couleur ; face_point[5] dedié à la profondeur
                    face_list.append(face_points)
        
            ##DO THE DRAWING HERE

            face_list.sort(key=lambda x: x[-1], reverse=True)
            #slicing lists is a bad idea
            for face in face_list: #on ne dessine que les 3 faces maximum visibles simultanément -> pls vrais avec un modele contenant masse faces
                #TODO = use canvas.move
                #TODO = remove outline and make shader
                color = '#%02x%02x%02x' % face[-2]
                canvas.create_polygon(face[:-2], fill=color, outline="black", tag="faces")



    ##tLOL = time.time()
    ######################################################################
    #on remet l'image à 0
    root.update()
    canvas.delete("faces")
    ###################################################################### super lent, tank les fps
    ##print(( time.time()-tLOL ), "canvas delete")

    frameRate += time.time()-t0
    i+=1
    if i > 50 :
        print(1/((frameRate/i)+1e-10),"fps")
        i=0
        frameRate=0
