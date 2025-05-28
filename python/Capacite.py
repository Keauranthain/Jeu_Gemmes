import json
import os

capacites_jeu = {}

class Capacite_class():
    def __init__(self, nom, clef, force=0, magie=0, temps=0,
                 cible_autre=True, cible_sois=False, soin=False,
                 magique=True, mana=None, endurance=None):
        self.nom = nom
        self.clef = clef
        self.force = force
        self.magie = magie
        self.temps = temps
        self.cible_autre = cible_autre
        self.cible_sois = cible_sois
        self.soin = soin
        self.magique = magique

        self.mana = mana if mana is not None else magie * (temps - 10) * -1
        self.endurance = endurance if endurance is not None else force * (temps - 10) * -1

    def __str__(self):
        return f"nom : {self.nom}, clef : {self.clef}, force : {self.force}, magie : {self.magie}, endurance : {self.endurance}, mana : {self.mana}, temps : {self.temps}, cible sois : {self.cible_sois}, magique : {self.magique}"

def capacite(clef: str):
    return capacites_jeu[clef]

def setup():
    chemin_json = "ressources/capacite.json"
    with open(chemin_json, encoding="utf-8") as f:
        data = json.load(f)

    for section in ["capacite_basique", "capacite_magique", "capacite_physique"]:
        for clef, contenu in data.get(section, {}).items():
            capacites_jeu[clef] = Capacite_class(
                nom=contenu.get("nom", clef),
                clef=clef,
                force=contenu.get("force", 0),
                magie=contenu.get("magie", 0),
                temps=contenu.get("temps", 0),
                cible_autre=contenu.get("cible_autre", True),
                cible_sois=contenu.get("cible_sois", False),
                soin=contenu.get("soin", False),
                magique=contenu.get("magique", True),
                mana=contenu.get("mana"),
                endurance=contenu.get("endurance")
            )

setup()
