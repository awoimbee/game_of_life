###########################################################################################################
# Maillet William - Test du jeu de la vie, code expérimental                                              #
###########################################################################################################
# Prérequis à savoir avant de lire le code, afin de le comprendre :                                       #
#                                                                                                         #
# On considère que chaque cellule possède une valeur : 1 ou 0. Si elle possède la valeur 1, elle est      #
# vivante, si elle possède la valeur 0 elle est morte/n'existe pas. Le principe appliqué est de           #
# construire un tableau en '2D' avec des listes, et on a deux fonctions qui s'occupent de mettre en place #
# tout le fonctionnement du progamme. La première fonction s'occupe d'afficher le tableau d'après les     #
# valeurs qu'il contient, et la seconde fonction a pour but d'appliquer les règles du jeu de la vie       #
#                                                                                                         #
###########################################################################################################

#Importation de divers modules utiles
from tkinter import *
from random import randint
import time
import threading


def display():
    "Affiche un tableau dans le canvas à partir de la liste"
    global board

    canvas.delete("cell")
    x, y = 0, 0
    #Parcours du tableau de long en large
    for row in range(len(board)):
        for column in range(len(board[0])):

            #Cas d'une case morte
            if board[row][column] == 0:
                canvas.create_rectangle(x, y, x+cPix, y+cPix, fill="white", tag="cell")

            #Cas d'une case vivante
            if board[row][column] == 1:
                canvas.create_rectangle(x, y, x+cPix, y+cPix, fill="black", tag="cell")

            #On passe a la cellule suivante
            x += cPix
            #Retour à la ligne
            if x >= caseNumber*cPix:
                x = 0
        y += cPix
    #Affichage final
    root.update()
    time.sleep(0.05)



def neighborsFinding():
    "Chercher voisins + calculer couleur nouvelle case"
    global keepgoing, board, step
    keepgoing = True

    while keepgoing:
        #Parcours du tableau de long en large
        board_new=board
        for x in range(len(board)):
            for y in range(len(board[0])):

                neighbors = 0 #On initialise à 0 voisins

                #Parcours des voisins dans un rayon de 1, soit 3x3 cases
                for i in range(-1, 2): #Test des voisins par ligne.
                    for j in range(-1, 2): #Test voisins dans cases dans les lignes
                        neighbors+=board[(x+i+caseNumber)%caseNumber][(y+j+caseNumber)%caseNumber]

                #Retrait de la cellule étudiée (pas voisine)
                neighbors -= board[x][y]

                if neighbors!=0 : print(str(neighbors))
                #Application des règles du jeu de la vie
                if board[x][y]==1 and neighbors<2:
                    board_new[x][y] = 0
                elif board[x][y]==1 and neighbors>3:
                    board_new[x][y] = 0
                elif board[x][y] == 0 and neighbors==3:
                    board_new[x][y] = 1
                else:
                    board_new[x][y] = board[x][y]

        #Mise à jour de l'ancien tableau
        board=board_new
        #Mise à jour de l'étape et de l'état
        step += 1
        state.set("En cours" + " (étape "+ str(step) + ")")
        #Affichage
        display()



def stop():
    "Arrête le programme grâce à un interrupteur"
    global keepgoing, step
    keepgoing = False
    state.set("Arrêtée" + " (étape "+ str(step) + ")")



def changeColor(event):
    "Change la couleur de la case cliquée"
    global board

    coordX = event.y
    coordY = event.x
    canvCoords.set("Coordonnées : " + str(coordX) + " ; " + str(coordY))

    boardX = coordX//caseNumber
    boardY = coordY//caseNumber
    boardCoords.set("Dans le tableau : " + str(boardX) + " ; " + str(boardY))

    if board[boardX][boardY]==0:
        board[boardX][boardY] = 1

    elif board[boardX][boardY]==1:
        board[boardX][boardY] = 0
    display()



def clearAll():
    "Efface toute les cellules"
    global board, step
    step = 0
    board = [[0 for i in range(caseNumber)] for j in range(caseNumber)]
    display()





#####------FENETRE PRINCIPALE-----#####

if __name__ == "__main__":

    ###-- INITIALISATION DES VARIABLES --####
    cPix = 30 #Nombre de pixels d'une case
    caseNumber = 30 #Nombre de cases
    keepgoing=True #Interrupteur
    step = 0 #Étape
    root = Tk()
    root.title("Le Jeu de La Vie")
    board = [[0 for i in range(caseNumber)] for j in range(caseNumber)] #Tableau



    ###-- TALBEAU --###
    canvas = Canvas(root, width=cPix*caseNumber, height=cPix*caseNumber, bg="white")
    canvas.grid(column=1, row=1, padx=5, pady=5, rowspan=3)
    canvas.bind("<Button-1>", changeColor) #Localisation des clics dans le canvas



    ###-- INTERFACE INTERACTIONS UTILISATEUR/PROGRAMME --###
    userPart = LabelFrame(root, bd=2, text="Utilisateur")
    userPart.grid(column=2, row=1, padx=5, pady=5, sticky=N)
    #Bouton de lancement
    launchButton = Button(userPart, text="Lancer la simulation", command=neighborsFinding)
    launchButton.grid(column=1, row=1, padx=7, pady=5)
    #Bouton de stop
    stopButton = Button(userPart, text="Stopper la simulation", command=stop)
    stopButton.grid(column=1, row=2, padx=7, pady=5)
    #Bouton de clear
    clearButton = Button(userPart, text="Effacer tout", command=clearAll)
    clearButton.grid(column=1, row=3, padx=7, pady=5)



    ###-- INTERFACE DÉVELOPPEMENT --###
    devPart = LabelFrame(root, bd=2, text="Développeur")
    devPart.grid(column=2, row=2, padx=5, pady=5, sticky=N)
    #Coordonnées dans le canvas
    canvCoords = StringVar()
    canvCoords.set("Coordonnées :")
    cDisp1 = Label(devPart, textvariable=canvCoords)
    cDisp1.grid(column=1, row=1, padx=7, pady=5)
    #Coordonnées dans le tableau
    boardCoords = StringVar()
    boardCoords.set("Dans le tableau :")
    cDisp2 = Label(devPart, textvariable=boardCoords)
    cDisp2.grid(column=1, row=2, padx=7, pady=5)



    ###-- ÉTAT DE LA SIMULATION --###
    statePart = LabelFrame(root, bd=2, text="État de la simulation")
    statePart.grid(column=2, row=3, padx=5, pady=5, sticky=N)
    state = StringVar()
    state.set("Arrêteée")
    stateDisplay = Label(statePart, textvariable=state)
    stateDisplay.grid(column=1, row=1, padx=7, pady=5)





    #Activation du gestionnaire d'évènement de la fenêtre
    display()
    root.mainloop()
