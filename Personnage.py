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
        self.magie = races_global[race]["magie"] + races_global[race][f"magie_{self.genre}"]
        self.resistance_magique = races_global[race]["resistance_magique"] + races_global[race][f"resistance_magique_{self.genre}"]
        self.incantation = races_global[race]["incantation"] + races_global[race][f"incantation_{self.genre}"]
        self.mana_total = races_global[race]["mana"] + races_global[race][f"mana_{self.genre}"]
        self.mana = self.mana_total
        self.force = races_global[race]["force"] + races_global[race][f"force_{self.genre}"]
        self.resistance = races_global[race]["resistance"] + races_global[race][f"resistance_{self.genre}"]
        self.agilite = races_global[race]["agilite"] + races_global[race][f"agilite_{self.genre}"]
        self.endurance_total = races_global[race]["endurance"] + races_global[race][f"endurance_{self.genre}"]
        self.endurance = self.endurance_total
        self.vie_total = races_global[race]["vie"] + races_global[race][f"vie_{self.genre}"]
        self.vie = self.vie_total
        self.capacite = []
        for capacite_clef in races_global[race]["capacite_base"]:
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
            for k in range (len(liste_temporaire)):
                print(f"{k} : {liste_temporaire[k].nom}, mana : {liste_temporaire[k].mana},"
                      f" endurance : {liste_temporaire[k].endurance}")
            result = choix_nombre(max = len(liste_temporaire)-1, question = "Capacité : ")
            return liste_temporaire[result]
        return self.capacite[0]