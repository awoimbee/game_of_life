###########################################################################################################
# Maillet William - Arthur Woimbée - JEU DE LA VIE 2D ET 3D                                               #
###########################################################################################################


#Importation de divers modules utiles
import tkinter
import time
import show3D


##########################################
#   FONCTIONS DU JEU DE LA VIE EN 2D     #
##########################################

def display():
    "Affiche un tableau dans le canvas à partir de la liste"
    global board

    #Effacer toute les cellules
    canvas.delete("cell")

    #Coordonnées dans le canvas qui servent à placer les carrés
    x, y = 0, 0
    #Parcours du tableau de long en large
    for row in range(len(board)):
        for column in range(len(board[0])):

            #On trace seulement si la case est vivante
            if board[row][column] == 1:
                canvas.create_rectangle(x, y, x+caseSize, y+caseSize, fill="black", tag="cell", outline="grey")

            #On passe a la cellule suivante
            x += caseSize

            #Retour à la ligne
            if x >= boardWidth*caseSize:
                x = 0

        y += caseSize

    #Affichage final
    time.sleep(0.02)
    root.update()

def neighborsFinding():
    "Chercher voisins + calculer couleur nouvelle case"
    global keepgoing, step, board, boardWidth, boardHeight

    #Démarrage du processus
    keepgoing = True

    #Calcul des voisins
    while keepgoing:

        #Copie intégrale du tableau
        board_new=[[0 for i in range(boardWidth)] for j in range(boardHeight)]

        #Parcours du tableau de long en large
        for row in range(len(board)):
            for column in range(len(board[0])):

                #Voisins initialisés à 0
                neighbors = 0

                #Parcours des voisins dans un rayon de 1, soit 3x3 cases
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        #Ajout de la valeur de la case à "neighbors"
                        neighbors+=board[(row+i+boardHeight)%boardHeight][(column+j+boardWidth)%boardWidth]

                #Retrait de la cellule étudiée (pas voisine)
                neighbors -= board[row][column]

                #Application des règles du jeu de la vie
                if board[row][column]==1 and (neighbors<2 or neighbors >3):
                    board_new[row][column] = 0    #Mort car pas assez de cellules voisines

                elif board[row][column]==1 and (neighbors==2 or neighbors==3):
                    board_new[row][column] = 1    #Vie qui continue

                elif board[row][column]==0 and neighbors==3:
                    board_new[row][column] = 1    #Naissance car 3 cellules voisines

                else:
                    board_new[row][column] = board[row][column]

        #Mise à jour de l'ancien tableau
        board=board_new

        #Actualisation du tableau de la partie 3D
        show3D.newLine(board)

        #Mise à jour de l'étape et de l'état
        step += 1
        state.set("En cours" + " (étape "+ str(step) + ")")

        #Affichage
        display()

def stop():
    "Arrête le programme grâce à un interrupteur"
    global keepgoing, step

    #On arrête le processus de calcul des voisins
    keepgoing = False
    state.set("Arrêtée" + " (étape "+ str(step) + ")")

def changeColor(event):
    "Change la couleur de la case cliquée"

    #Affichage des coordonnées dans le canvas
    canvCoords.set("Coordonnées : " + str(event.x) + " ; " + str(event.y))

    #Calcul et affichage des coordonnées dans la case dans le tableau
    boardColumn = event.x//caseSize
    boardRow = event.y//caseSize
    boardCoords.set("Dans le tableau : " + str(boardColumn) + " ; " + str(boardRow))

    #Si on clique sur une case blanche, elle devient noire
    if board[boardRow][boardColumn]==0:
        board[boardRow][boardColumn] = 1

    #Si on clique sur une case noire, elle devient blanche
    elif board[boardRow][boardColumn]==1:
        board[boardRow][boardColumn] = 0

    #Affichage
    show3D.newLine(board)
    display()

def clearAll():
    "Efface toute les cellules"
    global board, step

    #Ré-initialisation des étapes
    step = 0
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Affichage
    display()

def ship():
    "Trace un vaisseau spatial dans le jeu de la vie"
    global board

    #Centre du vaisseau, au centre du canvas
    middleX = boardWidth//2
    middleY = boardHeight//2
    #Remise à 0 du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Ouverture d'un fichier qui contient des coordonnées
    f = open("ship.txt", "r")
    shipY, shipX = [], []
    #Ajout de chaques coordonnées dans une liste
    for l in f:
        row = l.split() #Transformation d'un caractère en liste
        shipY.append(row[0]) #Ajout de la première coordonnée
        shipX.append(row[1]) #De la deuxième

    #Traçage du vaisseau dans le canvas
    for i in range(len(shipY)):
        board[middleY+int(shipY[i])][middleX+int(shipX[i])] = 1

    display()


def clock():
    "Trace un vaisseau spatial dans le jeu de la vie"
    global board

    #Centre du vaisseau, au centre du canvas
    middleX = boardWidth//2
    middleY = boardHeight//2
    #Remise à 0 du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]

    #Ouverture d'un fichier qui contient des coordonnées
    f = open("clock.txt", "r")
    clockY, clockX = [], []
    #Ajout de chaques coordonnées dans une liste
    for l in f:
        row = l.split() #Transformation d'un caractère en liste
        clockY.append(row[0]) #Ajout de la première coordonnée
        clockX.append(row[1]) #De la deuxième

    #Traçage du vaisseau dans le canvas
    for i in range(len(clockY)):
        board[middleY+int(clockY[i])][middleX+int(clockX[i])] = 1

    display()
   
##########################################
#          PROGRAMME PRINCIPAL           #
##########################################

if __name__ == "__main__":

    ######## INITIALISATION DES VARIABLES ########
    #Taille d'une case en pixels
    caseSize = 10
    #Largeur du tableau
    boardWidth = 90
    #Hauteur du tableau
    boardHeight = 30
    #Interrupteur
    keepgoing=True
    #Étapes
    step = 0
    #Initialisation de la fenêtre
    root = tkinter.Tk()
    root.title("Le Jeu de La Vie")
    #Fond de la fenêtre
    root.configure(background="grey")
    #Initialisation du tableau
    board = [[0 for i in range(boardWidth)] for j in range(boardHeight)]
    #Initialisation du jeu de la vie en 3D
    show3D.initialise(700,900)



    ######## TABlEAU ########
    canvas = tkinter.Canvas(root, width=caseSize*boardWidth, height=caseSize*boardHeight, bg="white", bd=0, highlightthickness=0)
    canvas.grid(column=1, row=1, padx=2, pady=2, columnspan=100)
    canvas.bind("<Button-1>", changeColor) #Localisation des clics dans le canvas3
    canvas.bind("<B1-Motion>", changeColor)


    ######## INTERFACE INTERACTIONS UTILISATEUR/PROGRAMME ########
    userPart = tkinter.LabelFrame(root, bd=2, text="Utilisateur", bg="grey", fg="white", font=("Calibri", 12))
    userPart.grid(column=100, row=2, padx=5, pady=2, sticky=tkinter.W)

    #Bouton de lancement
    launchButton = tkinter.Button(userPart, text="Lancer la simulation", command=neighborsFinding, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    launchButton.grid(column=1, row=1, padx=7, pady=5)
    #Bouton de stop
    stopButton = tkinter.Button(userPart, text="Stopper la simulation", command=stop, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    stopButton.grid(column=1, row=2, padx=7, pady=5)
    #Bouton de clear
    clearButton = tkinter.Button(userPart, text="Effacer tout", command=clearAll, bg="#545556", fg="white", relief="flat", font=("Calibri", 12))
    clearButton.grid(column=1, row=3, padx=7, pady=5)



    ######## INTERFACE INFORMATION ########
    devPart = tkinter.LabelFrame(root, bd=2, text="Informations", bg="grey", fg="white", font=("Calibri", 12))
    devPart.grid(column=99, row=2, padx=5, pady=2, sticky=tkinter.W)

    #Coordonnées dans le canvas
    canvCoords = tkinter.StringVar()
    canvCoords.set("Coordonnées :")
    cDisp1 = tkinter.Label(devPart, textvariable=canvCoords, bg="grey", fg="white", font=("Calibri", 12))
    cDisp1.grid(column=1, row=1, padx=7, pady=5)
    #Coordonnées dans le tableau
    boardCoords = tkinter.StringVar()
    boardCoords.set("Dans le tableau :")
    cDisp2 = tkinter.Label(devPart, textvariable=boardCoords, bg="grey", fg="white", font=("Calibri", 12))
    cDisp2.grid(column=1, row=2, padx=7, pady=5)



    ######## ÉTAT DE LA SIMULATION ########
    statePart = tkinter.LabelFrame(devPart, bd=2, text="État de la simulation", bg="grey", fg="white", font=("Calibri", 12))
    statePart.grid(column=1, row=3, padx=5, pady=5, sticky=tkinter.W)

    state = tkinter.StringVar()
    state.set("Arrêteée")
    stateDisplay = tkinter.Label(statePart, textvariable=state, bg="grey", fg="white", font=("Calibri", 12))
    stateDisplay.grid(column=1, row=1, padx=7, pady=5)

    ######## BOUTON DE LA SIMULATION 3D ########
    tkinter.Button(userPart, text="Visualisation en 3D", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=show3D.launchWindow).grid(row=1, column=2, padx=5, pady=5)

    ######## BOUTONS POUR DIVERSES FORMES ########
    tkinter.Button(userPart, text="Vaisseau", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=ship).grid(row=2, column=2, padx=5, pady=5)
    tkinter.Button(userPart, text="Horloge", bg="#545556", fg="white", font=("Calibri", 12), relief="flat", command=clock).grid(row=3, column=2, padx=5, pady=5)
    

    #Fenêtre non-redimensionnable
    root.resizable(False, False)

    ######## TRACAGE DU QUADRILLAGE ########
    #Traçage du quadrillage vertical
    a,b = 0,0
    for i in range(len(board)):
        for j in range(len(board[0])):
            canvas.create_line(a, b, a, b+boardHeight*caseSize, fill="grey")
            a += caseSize
    #Traçage d'un quadrillage horizontal
    a, b = 0,0
    for i in range(len(board)):
        for j in range(len(board[0])):
            canvas.create_line(a, b, a+boardWidth*caseSize, b, fill="grey")
            b += caseSize



    #Activation du gestionnaire d'évènement de la fenêtre
    display()
    root.mainloop()
