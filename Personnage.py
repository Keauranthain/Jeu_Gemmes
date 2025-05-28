from Capacite import capacite
from Ressource import races_global
from Basique import choix_nombre

class Personnage():
    def __init__(self, nom:str, race:str = "humain", joueur = False,male:bool = False,female:bool = False):

        if male or not(female):
            self.genre = "male"
        else:
            self.genre = "female"
        self.nom = nom
        self.race = race

        base = races_global.get(race, {})

        self.magie = base.get("magie", 0) + base.get(f"magie_{self.genre}", 0)
        self.resistance_magique = base.get("resistance_magique", 0) + base.get(f"resistance_magique_{self.genre}", 0)
        self.incantation = base.get("incantation", 0) + base.get(f"incantation_{self.genre}", 0)
        self.mana_total = base.get("mana", 0) + base.get(f"mana_{self.genre}", 0)
        self.mana = self.mana_total
        self.force = base.get("force", 0) + base.get(f"force_{self.genre}", 0)
        self.resistance = base.get("resistance", 0) + base.get(f"resistance_{self.genre}", 0)
        self.agilite = base.get("agilite", 0) + base.get(f"agilite_{self.genre}", 0)
        self.endurance_total = base.get("endurance", 0) + base.get(f"endurance_{self.genre}", 0)
        self.endurance = self.endurance_total
        self.vie_total = base.get("vie", 0) + base.get(f"vie_{self.genre}", 0)
        self.vie = self.vie_total

        self.capacite = []
        for capacite_clef in base.get("capacite_base", []):
            self.capacite.append(capacite(capacite_clef))

        self.joueur = joueur

    def __str__(self):
        return f"{self.nom}, {self.race}, {self.genre}, - Vie: {self.vie}/{self.vie_total}, Mana: {self.mana}/{self.mana_total}, Endurance: {self.endurance}/{self.endurance_total}"

    def capaciter_selecteur(self,mana,endurance):
        liste_temporaire = []
        for k in self.capacite:
            if k.mana<=mana and k.endurance<=endurance:
                liste_temporaire.append(k)
        if self.joueur:
            print(f"Endurance: {endurance}/{self.endurance_total}\nMana: {mana}/{self.mana_total}\n")
            for k in range (len(liste_temporaire)):
                print(f"{k} : {liste_temporaire[k].nom}, mana : {liste_temporaire[k].mana},"
                      f" endurance : {liste_temporaire[k].endurance}")
            result = choix_nombre(max = len(liste_temporaire)-1, question = "Capacité : ")
            return liste_temporaire[result]
        return self.capacite[0]