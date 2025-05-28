import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

fichier_json = os.path.join(os.path.dirname(__file__), "..", "ressources", "race.json")
fichier_json = os.path.abspath(fichier_json)

def charger_races():
    try:
        with open(fichier_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sauvegarder_races(races):
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(races, f, indent=2, ensure_ascii=False)

def main():
    def charger_race_selection(event):
        race = combo_race.get()
        if race not in races:
            return
        champ_nom.delete(0, tk.END)
        champ_nom.insert(0, race)
        data = races[race]

        check_var.set(data.get("magique", False))

        for cle in champs_normaux:
            for type_ in ["", "_male", "_female"]:
                champ = cle + type_ if type_ else cle
                val = data.get(champ, "")
                entrees[cle][type_].delete(0, tk.END)
                entrees[cle][type_].insert(0, str(val))

        for cle in tranches_age:
            val = data.get(cle, "")
            entrees[cle][""].delete(0, tk.END)
            entrees[cle][""].insert(0, str(val))

        capacite = data.get("capacite_base", [])
        entree_capacite.delete(0, tk.END)
        entree_capacite.insert(0, ", ".join(capacite))

    def sauvegarder_race():
        race = champ_nom.get().strip()
        if not race:
            messagebox.showerror("Erreur", "Nom de race requis.")
            return

        nouvelle_race = {"magique": check_var.get()}

        for cle in champs_normaux:
            for type_ in ["", "_male", "_female"]:
                entree = entrees[cle][type_]
                texte = entree.get().strip()
                if texte == "":
                    continue
                champ = cle + type_ if type_ else cle
                if texte.isdigit():
                    nouvelle_race[champ] = int(texte)
                else:
                    try:
                        nouvelle_race[champ] = float(texte)
                    except:
                        nouvelle_race[champ] = texte

        for cle in tranches_age:
            texte = entrees[cle][""].get().strip()
            if texte:
                if texte.isdigit():
                    nouvelle_race[cle] = int(texte)
                else:
                    try:
                        nouvelle_race[cle] = float(texte)
                    except:
                        nouvelle_race[cle] = texte

        capacite_texte = entree_capacite.get().strip()
        if capacite_texte:
            nouvelle_race["capacite_base"] = [x.strip() for x in capacite_texte.split(",") if x.strip()]

        races[race] = nouvelle_race
        sauvegarder_races(races)
        messagebox.showinfo("Succès", f"Race '{race}' enregistrée.")
        combo_race["values"] = list(races.keys())

    champs_normaux = [
        "vie", "mana", "endurance",
        "force", "agilite", "resistance", "charisme",
        "magie", "resistance_magique", "incantation", "intelligence"
    ]

    tranches_age = ["enfance", "adolescence", "adulte", "vieillesse", "esperance_de_vie"]

    races = charger_races()

    fenetre = tk.Tk()
    fenetre.title("Éditeur de Races")

    tk.Label(fenetre, text="Nom de la race").grid(row=0, column=0)
    champ_nom = tk.Entry(fenetre, width=20)
    champ_nom.grid(row=0, column=1)

    combo_race = ttk.Combobox(fenetre, values=list(races.keys()))
    combo_race.grid(row=0, column=2, columnspan=2)
    combo_race.bind("<<ComboboxSelected>>", charger_race_selection)

    check_var = tk.BooleanVar()
    check_magie = tk.Checkbutton(fenetre, text="Magique", variable=check_var)
    check_magie.grid(row=1, column=0, columnspan=4, sticky="w")

    tk.Label(fenetre, text="Champ").grid(row=2, column=0)
    tk.Label(fenetre, text="Base").grid(row=2, column=1)
    tk.Label(fenetre, text="Male").grid(row=2, column=2)
    tk.Label(fenetre, text="Female").grid(row=2, column=3)

    entrees = {}
    ligne = 3
    for cle in champs_normaux:
        tk.Label(fenetre, text=cle).grid(row=ligne, column=0)
        entrees[cle] = {
            "": tk.Entry(fenetre, width=10),
            "_male": tk.Entry(fenetre, width=10),
            "_female": tk.Entry(fenetre, width=10)
        }
        entrees[cle][""].grid(row=ligne, column=1)
        entrees[cle]["_male"].grid(row=ligne, column=2)
        entrees[cle]["_female"].grid(row=ligne, column=3)
        ligne += 1

    for cle in tranches_age:
        tk.Label(fenetre, text=cle).grid(row=ligne, column=0)
        entrees[cle] = {"": tk.Entry(fenetre, width=30)}
        entrees[cle][""].grid(row=ligne, column=1, columnspan=3, sticky="we")
        ligne += 1

    tk.Label(fenetre, text="capacite_base (séparées par des virgules)").grid(row=ligne, column=0, columnspan=2)
    entree_capacite = tk.Entry(fenetre, width=40)
    entree_capacite.grid(row=ligne, column=2, columnspan=2)
    ligne += 1

    bouton = tk.Button(fenetre, text="Sauvegarder la race", command=sauvegarder_race)
    bouton.grid(row=ligne, column=0, columnspan=4)

    fenetre.mainloop()
