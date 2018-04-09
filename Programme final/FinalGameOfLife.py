from tkinter import *
import os

def gameOfLife2D_start():
    "Démarre le jeu de la vie en 2D"
    os.system("2DGOL_William.py")

def gameOfLife3D_start():
    "Démarre le jeu de la vie en 3D"
    os.system("moteur3D.py")



if __name__ == "__main__":

    root = Tk()
    root.title("Le Jeu de la Vie")
    root.configure(background="grey")
    root.resizable(False, False)

    d2GOF = Button(root, text="Jeu de la vie\n[2D]", bg="#545556", fg="white", relief="flat", command=gameOfLife2D_start)
    d2GOF.configure(font=("Calibri", 20, "bold"), width=25, height=10)
    d2GOF.grid(row=1, column=1, padx=5, pady=10, sticky=W)

    d3GOF = Button(root, text="Jeu de la vie\n[3D]", bg="#545556", fg="white", relief="flat", command=gameOfLife3D_start)
    d3GOF.configure(font=("Calibri", 20, "bold"), width=25, height=10)
    d3GOF.grid(row=1, column=2, padx=5, pady=10, sticky=E)

    rootbg = PhotoImage(file="gameoflife.gif")
    rootbgDisp = Label(root, image=rootbg, width=750, height=100)
    rootbgDisp.grid(row=0, column=1, columnspan=2, padx=5, pady=10)
    rootbg2 = PhotoImage(file="gameoflife.gif")
    rootbgDisp2 = Label(root, image=rootbg2, width=750, height=100)
    rootbgDisp2.grid(row=2, column=1, columnspan=2, padx=5, pady=10)


    #Activation du gestionnaire d'évènements
    root.mainloop()
