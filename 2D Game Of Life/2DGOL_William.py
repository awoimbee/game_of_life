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


#Création et remplissage aléatoire du tableau
board = [[randint(0, 1) for i in range(20)] for j in range(20)]

def display():
    "Affiche un tableau dans le canvas à partir de la liste"
    x, y = 0, 0
    #Parcours du tableau de long en large
    for row in range(len(board)):
        for column in range(len(board[0])):

            #Cas d'une case morte
            if board[row][column] == 0:
                canvas.create_rectangle(x, y, x+c, y+c, fill="white")
                x += c
            #Cas d'une case vivante
            elif board[row][column] == 1:
                canvas.create_rectangle(x, y, x+c, y+c, fill="black")
                x += c

            #Retour à la ligne
            if x >= 20*c:
                x = 0
        y += c
    window.update()


def neighborsFinding():
    "Chercher voisins + calculer couleur nouvelle case"
    #Parcours du tableau de long en large
    for x in range(len(board)):
        for y in range(len(board[0])):

            neighbors = 0 #On initialise à 0 voisins

            #Parcours des voisins dans un rayon de 1, soit 3x3 cases
            for i in range(-1, 2): #Test des voisins par ligne
                for j in range(-1, 2): #Test voisins dans cases dans les lignes


                    neighbors +=
                    board[ (x+i+len(board)) % len(board) ]
                         [ (y+j+len(board[0])) % len(board[0]) ]

'''
Explication : On voudrait voisins += board[x+i][y+j], afin d'avoir les
coordonnées de la case du voisin et d'ajouter sa valeur à la variable
"neighbors", mais un soucis se pose : quand on est en extrémité de tableau, on
a des erreurs du type 'index out of range' car on sort du tableau, et la seule
manière de régler ceci est en ajoutant le nombre de colonne/de ligne et de
prendre le modulo de ce qu'il reste pour revenir en début de ligne et être sûr
de ne pas avoir d'erreur parce qu'on est sorti du tableau.
'''

            #Retrait de la cellule étudiée (pas voisine)
            neighbors -= board[x][y]

            #Application des règles du jeu de la vie
            if board[x][y]==0 and neighbors==3:
                board[x][y] = 1

            elif (board[x][y]==1 and neighbors==3) or
            (board[x][y]==1 and neighbors==2):
                board[x][y] = 1

            else:
                board[x][y] = 0

'''
Rappel des règles (d'après Wikipédia, mais cela pourra être changé par la suite)
: Une cellule morte possédant exactement trois voisines doit naître, et une
cellule vivante possédant deux ou trois voisine doit rester vivante. Les autres
cellules meurent.
'''

    #Après le calcul de toutes les nouvelles couleurs, affichage.
    display()


def loop():
    "Lance les étapes infinies"
    global a
    a = 1
    while a==1:
        neighborsFinding()

def stop():
    "Stop les étapes infinies"
    global a
    a = 0


#####------FENETRE PRINCIPALE-----#####

if __name__ == "__main__":
    c, a = 20, 1
    window = Tk()
    window.title("Test jeu de la vie William")

    #Le tableau généré aléatoirement
    canvas = Canvas(window, width=c*20, height=c*20, bg="white")
    canvas.grid(column=1, row=1, padx=10, pady=10, rowspan=10)
    display()
    #Bouton pour faire une étape
    stepButton = Button(window, text="Étape suivante", command=neighborsFinding)
    stepButton.grid(column=2, row=1, padx=10, pady=10, columnspan=2)

    #Bouton pour faire deux étapes
    infButton = Button(window, text="Lancer", command=loop)
    infButton.grid(column=2, row=2, padx=10, pady=10)

    stopButton = Button(window, text="Stop", command=stop)
    stopButton.grid(column=3, row=2, padx=10, pady=10)

    #Activation du gestionnaire d'évènement de ma fenêtre
    window.mainloop()

    loop()
