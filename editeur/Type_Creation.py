import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

fichier_json = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ressources", "type.json"))

def charger_types():
    try:
        with open(fichier_json, "r", encoding="utf-8") as f:
            contenu = f.read().strip()
            if not contenu:
                return {}
            return json.loads(contenu)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def sauvegarder_types(caps):
    with open(fichier_json, "w", encoding="utf-8") as f:
        json.dump(caps, f, indent=2, ensure_ascii=False)

def main():
    caps = charger_types()

    def maj_liste():
        toutes_cles.clear()
        toutes_cles.extend(caps.keys())
        combo_charge["values"] = sorted(toutes_cles)

    def charger_type(event=None):
        cle = combo_charge.get().strip()
        if not cle:
            return
        if cle in caps:
            donnees = caps[cle]
            for champ in champs:
                val = donnees.get(champ, "")
                if isinstance(val, list):
                    val = ", ".join(val)
                entrees[champ].delete(0, tk.END)
                entrees[champ].insert(0, val)
        else:
            messagebox.showinfo("Info", "Type non trouvé.")

    def sauvegarder():
        nom_type = entrees["nom"].get().strip()
        if not nom_type:
            messagebox.showerror("Erreur", "Le champ 'nom' est requis.")
            return

        nouvelle = {"nom": nom_type}
        for k in champs:
            v = entrees[k].get().strip()
            if not v:
                continue
            if k in ["faiblesse", "resistance"]:
                liste_valeurs = [x.strip() for x in v.split(",") if x.strip()]
                nouvelle[k] = liste_valeurs
            else:
                nouvelle[k] = v

        caps[nom_type] = nouvelle
        sauvegarder_types(caps)
        maj_liste()
        messagebox.showinfo("Succès", f"Type '{nom_type}' enregistré.")

    champs = ["nom", "adjectif", "adjectif_feminin", "faiblesse", "resistance"]
    fen = tk.Tk()
    fen.title("Éditeur de Types")
    cadre = tk.Frame(fen, padx=10, pady=10)
    cadre.pack(fill="both", expand=True)

    tk.Label(cadre, text="Charger existant").grid(row=2, column=0, sticky="w", pady=2)
    toutes_cles = []
    combo_charge = ttk.Combobox(cadre, values=toutes_cles, state="readonly")
    combo_charge.grid(row=2, column=1, pady=2)
    combo_charge.bind("<<ComboboxSelected>>", charger_type)

    entrees = {}
    row = 3
    for k in champs:
        tk.Label(cadre, text=k.capitalize()).grid(row=row, column=0, sticky="w", pady=2)
        ent = tk.Entry(cadre, width=30)
        ent.grid(row=row, column=1, pady=2)
        entrees[k] = ent
        row += 1

    btn_frame = tk.Frame(cadre, pady=10)
    btn_frame.grid(row=row, column=0, columnspan=2)
    tk.Button(btn_frame, text="Charger", command=charger_type, width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Sauvegarder", command=sauvegarder, width=12).pack(side="left", padx=5)

    cadre.columnconfigure(1, weight=1)
    maj_liste()
    fen.mainloop()

if __name__ == "__main__":
    main()
