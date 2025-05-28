import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

race_json = os.path.join(os.path.dirname(__file__), "..", "ressources", "race.json")
race_json = os.path.abspath(race_json)
cap_json = os.path.join(os.path.dirname(__file__), "..", "ressources", "capacite.json")
cap_json = os.path.abspath(cap_json)

def charger_races():
    try:
        with open(race_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def sauvegarder_races(races):
    with open(race_json, "w", encoding="utf-8") as f:
        json.dump(races, f, indent=2, ensure_ascii=False)

def charger_caps():
    try:
        with open(cap_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            caps = {}
            for cat in ("capacite_basique", "capacite_magique", "capacite_physique"):
                for k in data.get(cat, {}):
                    caps[k] = True
            return sorted(caps.keys())
    except FileNotFoundError:
        return []

def main():
    races = charger_races()
    all_caps = charger_caps()

    def charger_race_selection(event):
        race = combo_race.get()
        if race not in races:
            return
        champ_nom.delete(0, tk.END)
        champ_nom.insert(0, race)
        data = races[race]
        check_var.set(1 if data.get("magique", False) else 0)
        if check_var.get():
            check_magie.select()
        else:
            check_magie.deselect()
        for cle in champs_normaux:
            for suffix in ("", "_male", "_female"):
                e = entrees[cle][suffix]
                e.delete(0, tk.END)
                e.insert(0, str(data.get(cle + suffix, "")))
        for cle in tranches_age:
            e = entrees[cle][""]
            e.delete(0, tk.END)
            e.insert(0, str(data.get(cle, "")))
        entree_capacite.delete(0, tk.END)
        entree_capacite.insert(0, ", ".join(data.get("capacite_base", [])))

    def ajouter_capacite(event=None):
        sel = combo_cap.get().strip()
        if not sel:
            return
        existing = [c.strip() for c in entree_capacite.get().split(",") if c.strip()]
        if sel not in existing:
            existing.append(sel)
            entree_capacite.delete(0, tk.END)
            entree_capacite.insert(0, ", ".join(existing))

    def sauvegarder_race():
        race = champ_nom.get().strip()
        if not race:
            messagebox.showerror("Erreur", "Nom de race requis.")
            return
        nouvelle = {"magique": bool(check_var.get())}
        for cle in champs_normaux:
            for suffix in ("", "_male", "_female"):
                texte = entrees[cle][suffix].get().strip()
                if texte == "":
                    continue
                champ = cle + suffix
                if texte.isdigit():
                    nouvelle[champ] = int(texte)
                else:
                    try:
                        nouvelle[champ] = float(texte)
                    except ValueError:
                        nouvelle[champ] = texte
        for cle in tranches_age:
            texte = entrees[cle][""].get().strip()
            if texte == "":
                continue
            if texte.isdigit():
                nouvelle[cle] = int(texte)
            else:
                try:
                    nouvelle[cle] = float(texte)
                except ValueError:
                    nouvelle[cle] = texte
        caps = [x.strip() for x in entree_capacite.get().split(",") if x.strip()]
        if caps:
            nouvelle["capacite_base"] = caps
        races[race] = nouvelle
        sauvegarder_races(races)
        messagebox.showinfo("Succès", f"Race '{race}' enregistrée.")
        combo_race["values"] = list(races.keys())

    champs_normaux = [
        "vie", "mana", "endurance",
        "force", "agilite", "resistance", "charisme",
        "magie", "resistance_magique", "incantation", "intelligence"
    ]
    tranches_age = ["enfance", "adolescence", "adulte", "vieillesse", "esperance_de_vie"]

    fenetre = tk.Tk()
    fenetre.title("Éditeur de Races")

    tk.Label(fenetre, text="Nom de la race").grid(row=0, column=0, padx=5, pady=5)
    champ_nom = tk.Entry(fenetre, width=20)
    champ_nom.grid(row=0, column=1, padx=5, pady=5)

    combo_race = ttk.Combobox(fenetre, values=list(races.keys()), state="readonly")
    combo_race.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
    combo_race.bind("<<ComboboxSelected>>", charger_race_selection)

    check_var = tk.IntVar(value=0)
    check_magie = tk.Checkbutton(fenetre, text="Magique", variable=check_var)
    check_magie.grid(row=1, column=0, columnspan=4, sticky="w", padx=5, pady=5)
    if check_var.get():
        check_magie.select()
    else:
        check_magie.deselect()

    tk.Label(fenetre, text="Champ").grid(row=2, column=0, padx=5, pady=2)
    tk.Label(fenetre, text="Base").grid(row=2, column=1, padx=5, pady=2)
    tk.Label(fenetre, text="Male").grid(row=2, column=2, padx=5, pady=2)
    tk.Label(fenetre, text="Female").grid(row=2, column=3, padx=5, pady=2)

    entrees = {}
    ligne = 3
    for cle in champs_normaux:
        tk.Label(fenetre, text=cle).grid(row=ligne, column=0, padx=5, pady=2)
        entrees[cle] = {
            "": tk.Entry(fenetre, width=10),
            "_male": tk.Entry(fenetre, width=10),
            "_female": tk.Entry(fenetre, width=10)
        }
        entrees[cle][""].grid(row=ligne, column=1, padx=5, pady=2)
        entrees[cle]["_male"].grid(row=ligne, column=2, padx=5, pady=2)
        entrees[cle]["_female"].grid(row=ligne, column=3, padx=5, pady=2)
        ligne += 1

    for cle in tranches_age:
        tk.Label(fenetre, text=cle).grid(row=ligne, column=0, padx=5, pady=2)
        entrees[cle] = {"": tk.Entry(fenetre, width=30)}
        entrees[cle][""].grid(row=ligne, column=1, columnspan=3, padx=5, pady=2, sticky="we")
        ligne += 1

    tk.Label(fenetre, text="Ajouter capacité").grid(row=ligne, column=0, padx=5, pady=5)
    combo_cap = ttk.Combobox(fenetre, values=all_caps, state="readonly", width=30)
    combo_cap.grid(row=ligne, column=1, columnspan=2, padx=5, pady=5, sticky="we")
    combo_cap.bind("<<ComboboxSelected>>", ajouter_capacite)

    tk.Label(fenetre, text="capacite_base (séparées par des virgules)").grid(row=ligne+1, column=0, columnspan=2, padx=5, pady=2)
    entree_capacite = tk.Entry(fenetre, width=40)
    entree_capacite.grid(row=ligne+1, column=2, columnspan=2, padx=5, pady=2)
    ligne += 2

    tk.Button(fenetre, text="Sauvegarder la race", command=sauvegarder_race).grid(row=ligne, column=0, columnspan=4, padx=5, pady=10)

    fenetre.mainloop()

if __name__ == "__main__":
    main()
