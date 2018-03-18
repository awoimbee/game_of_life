import tkinter
from PIL import ImageTk, Image
import math, random
import time
import os
#import _thread



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

    cos = (math.cos(cam.rot[0]), math.cos(cam.rot[1]))
    sin = (math.sin(cam.rot[0]), math.sin(cam.rot[1]))
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

        x,z = x*cos[1]-z*sin[1], z*cos[1]+x*sin[1]   #x et z modifies par la rotation autour de y
        y,z = y*cos[0]-z*sin[0], z*cos[0]+y*sin[0]   #y et z modifies par la rotation autour de x

#il y a un probleme si l'angle cam.rot[1] est multiple de 3 ?!

        if z>0:
            #si z=0 on a une division par 0 et si z<0 alors l'affichage est hors champ
            f=SWidth/z #coefficient de stereoscopie 
            X,Y = int(x*f)+SWidth, int(y*f)+SHeight #position en pixels des sommets sur l'image 2D

            if X<WIDTH+SWidth and Y<HEIGHT+SHeight and X>-SWidth and Y>-SHeight: #peu d'impact sur framerate
                obj.depth = (x**2)+(y**2)+(z**2)
                #print(obj.depth, obj.color, "pos :", x,y,z)
                obj.show = True
    objects.sort(key=lambda x: x.depth, reverse=True) #on ordonne objects selon l'ordre de depth
    ############################################################# impact *très minime* sur le framerate




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
    depth=0
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
                ass = line[1:].split()
                for fuck in ass:
                    arr.append(float(fuck))
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
        self.vertices = [(x+X/2, -y-Y/2, -z-Z/2) for X,Y,Z in self.vertices]
        self.color=color



if __name__ == '__main__':
    WIDTH = 600
    HEIGHT = 600
    SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
    sensMouv = 1 #sensibilite des mouvements
    sensRot = 1/4 #sensibilite de la rotation
    colors  = ((255,0,0), (0,255,0), (0,0,255), (20,100,230), (50,150,50))

    cam = Camera((0,0,-3)) #position initiale de la caméra

#Crétation de la liste des objets à afficher
    objects = [] 
    ############################## 
    # for x in range(-5, 5):
    #     for z in range(-5, 5):
    #         objects.append(FloorPannel((x,0,z),(255,255,255)))
    ###############################
    for x in range(0,2):
        for z in range(0,2):
            for y in range(0,-2,-1):
                objects.append( Ext3DModel("cube",(x,y,z),random.choice(colors)) )

    #objects.extend( [Ext3DModel("cube",(0,0,0),((255,255,255))), Ext3DModel("cube",(2,0,0), (0,0,255)), Ext3DModel("cube",(-2,0,0), (0,255,0))] )        
    #objects.append(Ext3DModel("body_highpoly",(0,0,0),(255,255,255) ))




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



    cos = (0,0)
    sin = (1,1)
    #i,frameRate=0,0
    #fastCoeff=0
    while True:
        #t0 = time.time()

        #on calcule comment dessiner chaque cube        
        for obj in objects :
            if obj.show :
                # TODO = SKIP SOME POLY WHEN OBJECT IS FAR
                face_list=[] #contient : [points1, points2, ...] => [ [ (x,y),(x,y),(x,y),(x,y), tuple(couleur), int(profondeur) ], [ (x,y),...], ...]
                for face in obj.faces:
                    depth = 0
                    face_points = [] #contient 3 ou plus sommets a connecter -> (x,y),(x,y),(x,y)

                    #chaque point de la face a une normale, on fait la moyenne de ces normales pour avoir la normale de la face
                    nx,ny,nz = 0.,0.,0.
                    x,y,z=0,0,0
                    for n in range( len(face[1])-1 ):  # ! les listes commences à 1 dans les fichiers obj !
                        nx += obj.normals[face[1][n] -1][0]
                        ny += obj.normals[face[1][n] -1][1]
                        nz += obj.normals[face[1][n] -1][2]
                        x,y,z = x+obj.vertices[face[0][n] -1][0], y+obj.vertices[face[0][n] -1][1], z+obj.vertices[face[0][n] -1][2]

                    
                    x,y,z = x/len(face[1])-1 -cam.pos[0], y/len(face[1])-1 -cam.pos[1], z/len(face[1])-1 -cam.pos[2]  #on calcule l'origine de la droite normale à la face
                    nx,ny,nz = nx/len(face[1])-1, ny/len(face[1])-1, nz/len(face[1])-1

                    #On applique la formule de la rotation 2D au vecteur (on ne garde que nz car nx et ny seront quoi qu'il qrrive divisés par 0 doncx n'ont pas d'importance)
                    #nz = (nz*cos[1]+nx*sin[1]) *cos[0]+ny*sin[0]

                    #Si ß est l'angle entre 2 vecteurs u et n, cos(ß)=(u.n)/(||u||*||n||) or ici ||u||=||n||=1 ; Donc cos(ß)=(u.n)
                    #Aussi, u=lightsource=(0,0,1) ; donc u.n = uz*nz = nz
                    #On peut maintenant utiliser |cos(ß)| comme pourcentage de lumiere recue. Mais on ajoute aussi la distance de l'origine de la normale par rapport à la lumière
                    lightReceived = nz*nz - ((x**2)+(y**2)+(z**2))/10

                    faceColor=[]
                    for colorComponent in obj.color:
                        component = int(colorComponent*lightReceived)
                        if component>255:
                            component=255
                        elif component<0:
                            component=0

                        faceColor.append(component) 
                    faceColor=tuple(faceColor)

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
                        #si il n'y a pas au moins 1 des points qui sort de l'écran
                        face_points.extend( (faceColor, depth) ) #face_points[4] est dedié à la couleur ; face_point[5] dedié à la profondeur
                        face_list.append(face_points)
            
                ##DO THE DRAWING HERE
                face_list.sort(key=lambda x: x[-1], reverse=True)
                #slicing lists is a bad idea
                for face in face_list: #on ne dessine que les 3 faces maximum visibles simultanément -> pls vrais avec un modele contenant masse faces
                    #TODO = use canvas.move
                    canvas.create_polygon(face[:-2], fill='#%02x%02x%02x' % face[-2], tag="faces") #la couleur est transformée de RGB en hexadecimal



        ##tLOL = time.time()
        ######################################################################
        #on remet l'image à 0
        root.update()
        canvas.delete("faces")
        ###################################################################### super lent, tank les fps
        ##print(( time.time()-tLOL ), "canvas delete")

        #frameRate += time.time()-t0
        #i+=1
        #if i > 50 :
            #print(1/((frameRate/i)+1e-10),"fps")
            #i=0
            #frameRate=0
