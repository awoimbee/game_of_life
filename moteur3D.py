import tkinter
import PIL
from PIL import ImageTk, Image, ImageDraw

WIDTH = 800
HEIGHT = 800
SWidth, SHeight = WIDTH//2, HEIGHT//2 #semi width and semi height
SENSIBILITE = 1

#JE VOULAIS FAIRE UNE CLASSE SAUF QUE TKINTER C'EST DE LA MERDE N'ESTCE PAS ?

class Camera:
    def __init__(self, pos=(0,0,0), rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot) #rot=rotation

def keypress(event):
    print("keypress !!")
    #right left forward backward  up  down
    # ++X  --X    ++Z     --Z    ++Y  --Y
    if event.keysym == 'd':
        cam.pos[0]+=SENSIBILITE
    elif event.keysym == 'a':
        cam.pos[0]-=SENSIBILITE
    elif event.keysym == 'w':
        cam.pos[2]+=SENSIBILITE
    elif event.keysym == 's':
        cam.pos[2]-=SENSIBILITE
    elif event.keysym == 'q':
        cam.pos[1]+=SENSIBILITE
    elif event.keysym == 'e':
        cam.pos[1]-=SENSIBILITE

    elif event.keysym == 'Escape':
        root.destroy()

        

##Création de la fenetre
root = tkinter.Tk()
frame = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
root.bind("<Key>", keypress)
frame.pack()


# chaque frame sera PILimg
PILimg = Image.new('RGB', (WIDTH,HEIGHT), (255, 255, 255))


#sommets du cube selon le repere (x,y,z) puis les arretes du cube
vertices = (-1,1,-1),(1,1,-1),(1,-1,-1),(-1,-1,-1), (-1,1,1),(1,1,1),(1,-1,1),(-1,-1,1)
edges = (0,1),(1,2),(2,3),(3,0), (0,4), (1,5),(2,6),(3,7), (4,5),(5,6),(6,7),(7,4)

cam=Camera((0,0,-5))
i=0
while True:
    
    #framecount
    i+=1
    print(i, cam.pos)
    #position de ces sommets sur l'image 2D
    verticesPxPos = []

    for x,y,z in vertices:
        z+=6 #la camera est positionee a z=0, on ne veut pas etre dans le cube
        f=SWidth/z #un coefficient de putain de 3d machin la de comment ca ressort et tout putain en 3d stereoscopique on en parle bcp de cette merde
        x,y = int(x*f)+SWidth, int(y*f)+SHeight  #donne la position de x et y en pixels

        verticesPxPos.append([x,y]) #"position de ces sommets sur l'image 2D"
        PILimg.putpixel ((x,y), ( 0, 0, 0 )) #on met tout sur l'image


##    for edge in edges:
##        z+=6 #la camera est positionee a z=0, on ne veut pas etre dans le cube
##        f=SWidth/z #un coefficient de putain de 3d machin la de comment ca ressort et tout putain en 3d stereoscopique on en parle bcp de cette merde
##        x,y = int(x*f)+SWidth, int(y*f)+SHeight  #donne la position de x et y en pixels
##
##        verticesPxPos.append([x,y]) #"position de ces sommets sur l'image 2D"
##        PILimg.putpixel ((x,y), ( 0, 0, 0 )) #on met tout sur l'image




    draw = ImageDraw.Draw(PILimg)       
    for A,B in edges :                                             
        draw.line((verticesPxPos[A][0],verticesPxPos[A][1], verticesPxPos[B][0],verticesPxPos[B][1]), fill=128)
    del draw
    

    img = ImageTk.PhotoImage(PILimg)
    canvas.create_image(SWidth, SHeight, image=img) #jsp pq faut utiliser SW et SH

    #root.canvas.update_idletasks #affiche l'image WTF MAINTENANT IL VEUT PLUS UTILLISER CA KWELRFPHOWTGIUIHOGREUW
    root.update() #end

root.mainloop() #end
