import tkinter as tk
from Race_Creation import main as ouvrir_editeur_race

def lancer_editeur_race():
    ouvrir_editeur_race()

def main():
    fenetre = tk.Tk()
    fenetre.title("Outil de Création")

    bouton_race = tk.Button(fenetre, text="Éditeur de Races", command=lancer_editeur_race, width=30, height=2)
    bouton_race.pack(padx=20, pady=20)

    fenetre.mainloop()

if __name__ == "__main__":
    main()
