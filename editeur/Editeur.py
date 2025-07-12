import tkinter as tk
from editeur.Race_Creation import main as ouvrir_editeur_race
from editeur.Capacite_Creation import main as lancer_editeur_capacite
from editeur.Type_Creation import main as lancer_editeur_type

def lancer_editeur_race():
    ouvrir_editeur_race()

def main():
    fenetre = tk.Tk()
    fenetre.title("Outil de Création")

    bouton_race = tk.Button(fenetre, text="Éditeur de Races", command=lancer_editeur_race, width=30, height=2)
    bouton_race.pack(padx=20, pady=20)

    bouton_capacite = tk.Button(fenetre, text="Éditeur de Capacités", command=lancer_editeur_capacite, width=30,height=2)
    bouton_capacite.pack(padx=20, pady=10)

    bouton_capacite = tk.Button(fenetre, text="Éditeur de types", command=lancer_editeur_type, width=30, height=2)
    bouton_capacite.pack(padx=20, pady=10)

    fenetre.mainloop()

if __name__ == "__main__":
    main()
