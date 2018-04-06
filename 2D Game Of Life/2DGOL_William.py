###########################################################################################################
# Maillet William - Test du jeu de la vie                                                                 #
###########################################################################################################


#Importation de divers modules utiles
from tkinter import *
from random import randint
import time
import copy


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




def neighborsFinding():
    "Chercher voisins + calculer couleur nouvelle case"
    global keepgoing, step, board

    #Démarrage du processus
    keepgoing = True

    #Calcul des voisins
    while keepgoing:

        #Copie intégrale du tableau
        board_new= copy.deepcopy(board)

        #Parcours du tableau de long en large
        for row in range(len(board)):
            for column in range(len(board[0])):

                #Voisins initialisés à 0
                neighbors = 0

                #Parcours des voisins dans un rayon de 1, soit 3x3 cases
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        #Ajout de la valeur de la case à "neighbors"
                        neighbors+=board[(row+i+caseNumber)%caseNumber][(column+j+caseNumber)%caseNumber]

                #Retrait de la cellule étudiée (pas voisine)
                neighbors -= board[row][column]

                #Application des règles du jeu de la vie
                if board[row][column]==1 and (neighbors<2 or neighbors >3):
                    board_new[row][column] = 0    #Mort car pas assez de cellules voisines
                    
                elif board[row][column]==1 and (neighbors==2 or neighbors==3):
                    board_new[row][column] = 1    #Vie qui continue

                elif board[row][column]==0 and neighbors==3:
                    board_new[row][column] = 1    #Naissance car 3 cellules voisines

                

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

    #On arrête le processus de calcul des voisins
    keepgoing = False
    state.set("Arrêtée" + " (étape "+ str(step) + ")")



def changeColor(event):
    "Change la couleur de la case cliquée"

    #Affichage des coordonnées dans le canvas
    canvCoords.set("Coordonnées : " + str(event.x) + " ; " + str(event.y))
    
    #Calcul et affichage des coordonnées dans la case dans le tableau
    boardColumn = event.x//caseNumber
    boardRow = event.y//caseNumber
    boardCoords.set("Dans le tableau : " + str(boardColumn) + " ; " + str(boardRow))

    #Si on clique sur une case blanche, elle devient noire
    if board[boardRow][boardColumn]==0:
        board[boardRow][boardColumn] = 1
    #Si on clique sur une case noire, elle devient blanche
    elif board[boardRow][boardColumn]==1:
        board[boardRow][boardColumn] = 0

    #Affichage
    display()



def clearAll():
    "Efface toute les cellules"
    global board, step

    #Ré-initialisation des étapes
    step = 0
    board = [[0 for i in range(caseNumber)] for j in range(caseNumber)]

    #Affichage
    display()



#####------FENETRE PRINCIPALE-----#####

if __name__ == "__main__":

    ###-- INITIALISATION DES VARIABLES --####
    cPix = 30   #Nombre de pixels d'une case
    caseNumber = 30     #Nombre de cases
    keepgoing=True      #Interrupteur
    step = 0            #Étapes

    #Initialisation de la fenêtre
    root = Tk()
    root.title("Le Jeu de La Vie")
    #Initialisation du tableau
    board = [[0 for i in range(caseNumber)] for j in range(caseNumber)]



    ###-- TABlEAU --###
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
