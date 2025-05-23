import random as rnd
from Basique import obtenir_texte
import json

with open("ressources/capacite.json", "r", encoding="utf-8") as f:
    abilities = json.load(f)

spell_name = abilities["capacite_magique"]["5,4"]  # → "Flux"
print(spell_name)

print(obtenir_texte("fr",spell_name))

class Homme():
    def __init__(self, nom:str,joueur = False):
        self.nom = nom
        self.magie =  10
        self.resistance_magique = 10
        self.incantation = 10
        self.mana_total = 10
        self.mana = self.mana_total
        self.force = 10
        self.resistance = 10
        self.agilite = 10
        self.endurance_total = 10
        self.endurance = self.endurance_total
        self.vie_total = 10
        self.vie = self.vie_total
        self.capacite = [Capacite("coup de poing",5,0,1,2)]
        self.joueur = joueur

    def capaciter_selecteur(self):
        if self.joueur:
            for k in range (len(self.capacite)):
                print(f"{k} : {self.capacite[k].nom}")
            return self.capacite[int(input("Capacité : "))]
        return self.capacite[0]

class Capacite():
    def __init__(self,nom,force:int = 0,magie:int = 0,mana:int = 0, endurence:int = 0,temps:int = 0,
                 cible_autre:bool = True,cible_sois:bool = False,soin:bool = False,):
        self.nom = nom
        self.force = force
        self.magie = magie
        self.mana = magie*(temps-10)*-1
        self.endurence = endurence
        self.temps = temps
        self.cible_autre = cible_autre
        self.cible_sois = cible_sois
        self.soin = soin


class Combat():
    def __init__(self):
        self.combattant_1 = Homme(joueur=True,nom="Corentin")

    def temps(self,capacite,auteur):
        if capacite.magie > 0:
            t = (capacite.temps**2)/auteur.incantation
        else:
            t = (capacite.temps**2)/auteur.agilite
        return t
    def degat(self,capacite,cible,auteur):
        if capacite.magie > 0:
            d = (capacite.magie**1.5*auteur.magie)/(cible.resistance_magique**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        else:
            d = (capacite.force**1.5*auteur.force)/(cible.resistance**1.5)  * round(rnd.uniform(0.9, 1.1), 2)
        return round(d,2)

    def debut(self):
        combat_1 = self.combattant_1
        combat_2 = self.combattant_2

        print(f"{combat_1.nom} {combat_1.vie} / {combat_1.vie} VS {combat_2.nom} {combat_2.vie} / {combat_2.vie}")

        cap_1 = combat_1.capaciter_selecteur()
        cap_2 = combat_2.capaciter_selecteur()
        temps_1 = self.temps(cap_1,combat_1)
        temps_2 = self.temps(cap_2,combat_2)

        while(self.combattant_1.vie>0 and self.combattant_2.vie>0):
            if temps_1 < temps_2:
                temps_2 = temps_2-temps_1
                deg = self.degat(cap_1,combat_2,combat_1)
                print(f"{combat_1.nom} utilise {cap_1.nom} et inflige {deg}")
                combat_2.vie = round(combat_2.vie-deg,2)
                print(f"{combat_1.nom} {combat_1.vie} / {combat_1.vie_total} VS {combat_2.nom} {combat_2.vie} / {combat_2.vie_total}")
                if combat_1.vie > 0:
                    cap_1 = combat_1.capaciter_selecteur()
                    temps_1 = self.temps(cap_1, combat_1)
            else :
                temps_1 = temps_1 - temps_2
                deg = self.degat(cap_2, combat_1, combat_2)
                print(f"{combat_2.nom} utilise {cap_2.nom} et inflige {deg}")
                combat_1.vie = round(combat_1.vie - deg,2)
                print(f"{combat_1.nom} {combat_1.vie} / {combat_1.vie_total} VS {combat_2.nom} {combat_2.vie} / {combat_2.vie_total}")
                if combat_1.vie > 0 :
                    cap_2 = combat_2.capaciter_selecteur()
                    temps_2 = self.temps(cap_2, combat_2)
            print()
        if combat_1.vie<=0:
            print("Joueur mort")
        else:
            print("Goblin mort")

c = Combat()
#c.debut()