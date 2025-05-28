import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

fichier_json = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ressources", "capacite.json"))

def charger_capacites():
    try:
        with open(fichier_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"capacite_basique": {}, "capacite_magique": {}, "capacite_physique": {}}

def sauvegarder_capacites(caps):
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(caps, f, indent=2, ensure_ascii=False)

def main():
    caps = charger_capacites()

    def maj_liste():
        toutes_cles.clear()
        for bloc in caps.values():
            toutes_cles.extend(bloc.keys())
        combo_charge["values"] = sorted(toutes_cles)

    def charger_capacite(event=None):
        cle = combo_charge.get().strip()
        if not cle:
            return
        for cat, bloc in caps.items():
            if cle in bloc:
                categorie.set(cat)
                champ_clef.delete(0, tk.END)
                champ_clef.insert(0, cle)
                data = bloc[cle]
                for k in champs:
                    entrees[k].delete(0, tk.END)
                    entrees[k].insert(0, str(data.get(k, "")))
                for k in booleens:
                    valeurs_check[k].set(data.get(k, k in ["magique", "cible_autre"]))
                return
        messagebox.showinfo("Info", "Capacité non trouvée.")

    def sauvegarder():
        cle = champ_clef.get().strip()
        cat = categorie.get()
        if not cle:
            messagebox.showerror("Erreur", "Clé requise.")
            return
        nouvelle = {}
        for k in champs:
            v = entrees[k].get().strip()
            if v:
                try:
                    nouvelle[k] = int(v)
                except ValueError:
                    try:
                        nouvelle[k] = float(v)
                    except ValueError:
                        nouvelle[k] = v
        for k in booleens:
            nouvelle[k] = valeurs_check[k].get()
        caps[cat][cle] = nouvelle
        sauvegarder_capacites(caps)
        maj_liste()
        messagebox.showinfo("Succès", f"Capacité '{cle}' enregistrée.")

    champs = ["nom", "force", "magie", "temps", "mana", "endurance"]
    booleens = ["magique", "cible_sois", "cible_autre", "soin"]
    fen = tk.Tk()
    fen.title("Éditeur de Capacités")
    cadre = tk.Frame(fen, padx=10, pady=10)
    cadre.pack(fill="both", expand=True)
    tk.Label(cadre, text="Clé interne").grid(row=0, column=0, sticky="w", pady=2)
    champ_clef = tk.Entry(cadre, width=30)
    champ_clef.grid(row=0, column=1, pady=2)
    tk.Label(cadre, text="Catégorie").grid(row=1, column=0, sticky="w", pady=2)
    categorie = tk.StringVar(value="capacite_basique")
    combo_cat = ttk.Combobox(cadre, textvariable=categorie, values=list(caps.keys()), state="readonly")
    combo_cat.grid(row=1, column=1, pady=2)
    tk.Label(cadre, text="Charger existant").grid(row=2, column=0, sticky="w", pady=2)
    toutes_cles = []
    combo_charge = ttk.Combobox(cadre, values=toutes_cles, state="readonly")
    combo_charge.grid(row=2, column=1, pady=2)
    combo_charge.bind("<<ComboboxSelected>>", charger_capacite)
    entrees = {}
    row = 3
    for k in champs:
        tk.Label(cadre, text=k.capitalize()).grid(row=row, column=0, sticky="w", pady=2)
        ent = tk.Entry(cadre, width=30)
        ent.grid(row=row, column=1, pady=2)
        entrees[k] = ent
        row += 1
    valeurs_check = {}
    for k in booleens:
        default = k in ["magique", "cible_autre"]
        var = tk.BooleanVar(value=default)
        chk = tk.Checkbutton(cadre, text=k, variable=var)
        chk.grid(row=row, column=0, columnspan=2, sticky="w", pady=2)
        valeurs_check[k] = var
        row += 1
    btn_frame = tk.Frame(cadre, pady=10)
    btn_frame.grid(row=row, column=0, columnspan=2)
    tk.Button(btn_frame, text="Charger", command=charger_capacite, width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Sauvegarder", command=sauvegarder, width=12).pack(side="left", padx=5)
    cadre.columnconfigure(1, weight=1)
    maj_liste()
    fen.mainloop()

if __name__ == "__main__":
    main()
